#!/usr/bin/env python3
import os
import sys
import unittest
import json
from base64 import b64encode
from pathlib import Path

# --- 1) Make your app code importable ---
repo_root = Path(__file__).parent.resolve()
src_main  = repo_root / 'src' / 'main' / 'python'
if not src_main.is_dir():
    print("ERROR: src/main/python not found. Are you in the repo root?")
    sys.exit(1)
sys.path.insert(0, str(src_main))

# --- 2) Import factory and db ---
from uk.gov.hmcts.reform.dev.Application import create_app, db

class TaskApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create app & test client
        cls.app = create_app()
        cls.app.config.update(
            TESTING=True,
            BASIC_AUTH_USERNAME='admin',
            BASIC_AUTH_PASSWORD='secret'
        )
        # Recreate schema so it's empty
        with cls.app.app_context():
            db.drop_all()
            db.create_all()

        cls.client = cls.app.test_client()
        creds = b64encode(b"admin:secret").decode("utf-8")
        cls.auth = {"Authorization": f"Basic {creds}"}

    def test_root_serves_index(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b"Task Manager", rv.data)
        rv.close()

    def test_list_empty(self):
        rv = self.client.get("/tasks", headers=self.auth)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data), [])
        rv.close()

    def test_crud_and_status_flow(self):
        # CREATE
        r = self.client.post(
            "/tasks",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"title":"Foo","status":"pending","description":"Desc"})
        )
        self.assertEqual(r.status_code, 201)
        tid = json.loads(r.data)["id"]
        r.close()

        # GET
        r2 = self.client.get(f"/tasks/{tid}", headers=self.auth)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(json.loads(r2.data)["title"], "Foo")
        r2.close()

        # PATCH → in progress
        r3 = self.client.patch(
            f"/tasks/{tid}/status",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"status":"in progress"})
        )
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(json.loads(r3.data)["status"], "in progress")
        r3.close()

        # PATCH → done
        r4 = self.client.patch(
            f"/tasks/{tid}/status",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"status":"done"})
        )
        self.assertEqual(r4.status_code, 200)
        self.assertEqual(json.loads(r4.data)["status"], "done")
        r4.close()

        # INVALID PATCH
        r5 = self.client.patch(
            f"/tasks/{tid}/status",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"status":"BAD"})
        )
        self.assertEqual(r5.status_code, 400)
        r5.close()

        # DELETE
        r6 = self.client.delete(f"/tasks/{tid}", headers=self.auth)
        self.assertEqual(r6.status_code, 204)
        r6.close()

        # GET after delete → 404
        r7 = self.client.get(f"/tasks/{tid}", headers=self.auth)
        self.assertEqual(r7.status_code, 404)
        r7.close()

    def test_invalid_create(self):
        # missing status
        r = self.client.post(
            "/tasks",
            headers={**self.auth, "Content-Type":"application/json"},
            data=json.dumps({"title":"NoStatus"})
        )
        self.assertEqual(r.status_code, 400)
        r.close()

    def test_cors_preflight(self):
        rv = self.client.open("/tasks", method="OPTIONS")
        self.assertEqual(rv.status_code, 204)
        self.assertIn("Access-Control-Allow-Origin", rv.headers)
        rv.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)
