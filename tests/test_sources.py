"""核对业务资料的格式和交接标识。"""
import csv
import unittest
from pathlib import Path

SAMPLES = Path(__file__).resolve().parents[1] / "samples"
SCHEMAS = {'organizations': ['unit', 'group', 'control', 'sector', 'from_q', 'to_q', 'revision'], 'milestones': ['event', 'unit', 'quarter', 'kind', 'state', 'observed_on'], 'permissions': ['unit', 'scope', 'start', 'stop', 'expected_hours', 'version'], 'projects': ['program', 'resource', 'active_from', 'active_to', 'exclusive', 'contact_hours'], 'proposals': ['proposal', 'unit', 'program', 'quarter', 'status', 'contacted_on']}
REFERENCES = [('milestones', 'unit', 'organizations', 'unit'), ('permissions', 'unit', 'organizations', 'unit'), ('proposals', 'unit', 'organizations', 'unit'), ('proposals', 'program', 'projects', 'program')]
OBSERVED = [('organizations', 'unit', 'E2', 2), ('proposals', 'program', 'P1', 3), ('milestones', 'unit', 'E1', 3)]

class Sources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = {}
        for table, fields in SCHEMAS.items():
            with (SAMPLES / (table + ".csv")).open(encoding="utf-8", newline="") as stream:
                records = csv.DictReader(stream, strict=True)
                if records.fieldnames != fields:
                    raise ValueError(f"字段不一致：{table}")
                cls.tables[table] = list(records)

    def test_records_have_documented_columns(self):
        for table, rows in self.tables.items():
            with self.subTest(table=table):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_source_links(self):
        for left, field, right, target in REFERENCES:
            with self.subTest(table=left, field=field):
                keys = {row[field] for row in self.tables[left] if row[field]}
                self.assertTrue(keys)
                self.assertLessEqual(keys, {row[target] for row in self.tables[right]})

    def test_shared_source_records_are_available(self):
        for table, field, value, seen in OBSERVED:
            with self.subTest(table=table, field=field, value=value):
                self.assertGreaterEqual(sum(row[field] == value for row in self.tables[table]), seen)
