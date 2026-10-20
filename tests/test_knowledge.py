import unittest
from aila.knowledge import build_context, choose_kaomoji, retrieve_facts


class FakeRandom:
    def random(self):
        return 0.0
    def choice(self, seq):
        return seq[0]


class KnowledgeTests(unittest.TestCase):
    def test_origin(self):
        records, topic = retrieve_facts("为什么叫艾拉？")
        self.assertEqual(topic, "origin")
        self.assertEqual(records[0]["id"], "origin")

    def test_creator(self):
        records, topic = retrieve_facts("娄晟杰是谁？")
        self.assertEqual(topic, "creator")

    def test_followup(self):
        records, topic = retrieve_facts("他多大了？", previous_topic="creator")
        self.assertEqual(topic, "creator")
        self.assertTrue(any("未知" in text for text in records[0]["facts"]))

    def test_no_random_topic(self):
        self.assertEqual(retrieve_facts("你好呀")[0], [])

    def test_kaomoji_opt_out(self):
        self.assertIsNone(choose_kaomoji("好开心", 0))
        self.assertIsNone(choose_kaomoji("你好", 1, FakeRandom()))

    def test_kaomoji_emotional(self):
        self.assertIsNotNone(choose_kaomoji("好开心", 1, FakeRandom()))

    def test_context_hit(self):
        context, topic, ids = build_context("娄晟杰是谁", kaomoji_probability=0)
        self.assertEqual(ids, ["creator"])
        self.assertIn("创造者", context)


if __name__ == "__main__":
    unittest.main()
