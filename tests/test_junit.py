import tempfile
import unittest
from pathlib import Path

from flakeledger.junit import FAILED, PASSED, parse_file, parse_paths

SAMPLES = Path(__file__).resolve().parents[1] / "samples"

# A <testsuites> wrapper holding two suites. The first one carries the run
# markers as <property> entries, the second one carries none of its own.
WRAPPER_WITH_ONE_MARKED_SUITE = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="alpha">
    <properties>
      <property name="commit" value="aaaaaa"/>
      <property name="attempt" value="1"/>
    </properties>
    <testcase classname="tests.demo" name="test_p" time="1.0"/>
  </testsuite>
  <testsuite name="beta">
    <testcase classname="tests.demo" name="test_q" time="1.0">
      <failure message="boom"/>
    </testcase>
  </testsuite>
</testsuites>
"""

# The same wrapper, but the markers sit on the <testsuites> element itself.
WRAPPER_WITH_OWN_MARKERS = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <properties>
    <property name="commit" value="bbbbbb"/>
    <property name="attempt" value="2"/>
  </properties>
  <testsuite name="alpha">
    <testcase classname="tests.demo" name="test_p" time="1.0"/>
  </testsuite>
</testsuites>
"""


def _parse_text(xml: str):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "run.xml"
        path.write_text(xml, encoding="utf-8")
        return parse_file(path)


class TestJunitParsing(unittest.TestCase):
    def test_parses_attribute_metadata(self):
        results, warnings = parse_file(SAMPLES / "run-a1b2c3-attempt1.xml")
        self.assertEqual(warnings, [])
        self.assertEqual(len(results), 4)
        commits = {r.commit for r in results}
        self.assertEqual(commits, {"a1b2c3"})
        self.assertTrue(all(r.attempt == 1 for r in results))

    def test_status_detection(self):
        results, _ = parse_file(SAMPLES / "run-a1b2c3-attempt1.xml")
        by_id = {r.test_id: r for r in results}
        self.assertEqual(
            by_id["tests.payments.test_checkout.test_apply_coupon"].status,
            FAILED,
        )
        self.assertEqual(
            by_id["tests.payments.test_checkout.test_total_with_tax"].status,
            PASSED,
        )

    def test_reads_property_metadata_in_testsuites_wrapper(self):
        results, warnings = parse_file(SAMPLES / "run-99aa88-attempt1.xml")
        self.assertEqual(warnings, [])
        self.assertEqual(len(results), 3)
        self.assertTrue(all(r.commit == "99aa88" for r in results))
        self.assertTrue(all(r.attempt == 1 for r in results))

    def test_time_parsing(self):
        results, _ = parse_file(SAMPLES / "run-a1b2c3-attempt1.xml")
        header = next(
            r
            for r in results
            if r.name == "test_pdf_header"
        )
        self.assertAlmostEqual(header.time_seconds, 1.930, places=3)

    def test_parse_paths_is_sorted_and_complete(self):
        files = sorted(str(p) for p in SAMPLES.glob("*.xml"))
        results, _ = parse_paths(files)
        # a1b2c3: 4 + 4, d4e5f6: 4 + 4, b7c8d9: 3 + 3, 99aa88: 3 = 25 rows.
        self.assertEqual(len(results), 25)

    def test_suite_without_markers_does_not_inherit_a_sibling_suite_markers(self):
        results, warnings = _parse_text(WRAPPER_WITH_ONE_MARKED_SUITE)
        by_id = {r.test_id: r for r in results}
        self.assertEqual(by_id["tests.demo.test_p"].commit, "aaaaaa")
        # The 'beta' suite carries no markers of its own, so it must fall back
        # to the documented defaults rather than borrow the 'alpha' suite's.
        self.assertEqual(by_id["tests.demo.test_q"].commit, "unknown-commit")
        self.assertEqual(by_id["tests.demo.test_q"].attempt, 1)
        self.assertEqual(len(warnings), 1)
        self.assertIn("beta", warnings[0])

    def test_wrapper_with_own_markers_still_supplies_them_to_its_suites(self):
        results, warnings = _parse_text(WRAPPER_WITH_OWN_MARKERS)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].commit, "bbbbbb")
        self.assertEqual(results[0].attempt, 2)
        self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()
