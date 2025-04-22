#!/usr/bin/env python3
import unittest
import sys
import json
from base64 import b64encode
from pathlib import Path

from uk.gov.hmcts.reform.dev.Application import create_app

class TaskApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            TESTING=True,
            BASIC_AUTH_USERNAME='admin',
            BASIC_AUTH_PASSWORD='secret'
        )
        self.client = self.app.test_client()
        creds = b64encode(b"admin:secret").decode("utf-8")
        self.auth = {"Authorization": f"Basic {creds}"}

    def test_root_and_list(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b"Task Manager", rv.data)
        rv.close()

        rv2 = self.client.get("/tasks", headers=self.auth)
        self.assertEqual(rv2.status_code, 200)
        self.assertEqual(json.loads(rv2.data), [])
        rv2.close()

    def test_not_found(self):
        rv = self.client.get("/tasks/999", headers=self.auth)
        self.assertEqual(rv.status_code, 404)
        rv.close()

    def test_status_transitions(self):
        # create pending
        r1 = self.client.post(
            "/tasks",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"title":"X","status":"pending"})
        )
        self.assertEqual(r1.status_code, 201)
        tid = json.loads(r1.data)["id"]
        r1.close()

        # pending → in progress
        r2 = self.client.patch(
            f"/tasks/{tid}/status",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"status":"in progress"})
        )
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(json.loads(r2.data)["status"], "in progress")
        r2.close()

        # in progress → done
        r3 = self.client.patch(
            f"/tasks/{tid}/status",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"status":"done"})
        )
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(json.loads(r3.data)["status"], "done")
        r3.close()

        # invalid status
        r4 = self.client.patch(
            f"/tasks/{tid}/status",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"status":"bad"})
        )
        self.assertEqual(r4.status_code, 400)
        r4.close()

    def test_crud_and_errors(self):
        # invalid create (missing status)
        r0 = self.client.post(
            "/tasks",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"title":"NoStatus"})
        )
        self.assertEqual(r0.status_code, 400)
        r0.close()

        # create + delete + get
        rc = self.client.post(
            "/tasks",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"title":"Temp","status":"pending"})
        )
        tid = json.loads(rc.data)["id"]
        rc.close()

        rd = self.client.delete(f"/tasks/{tid}", headers=self.auth)
        self.assertEqual(rd.status_code, 204)
        rd.close()

        rg = self.client.get(f"/tasks/{tid}", headers=self.auth)
        self.assertEqual(rg.status_code, 404)
        rg.close()

    def test_cors_preflight(self):
        rv = self.client.open("/tasks", method="OPTIONS")
        self.assertEqual(rv.status_code, 204)
        self.assertIn("Access-Control-Allow-Origin", rv.headers)
        rv.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)
