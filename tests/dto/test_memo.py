from unittest import TestCase

from pydantic import ValidationError

from filedgr_xrpl_cli.dto.memo import MyMemo


class TestMyMemo(TestCase):

    def test_serialization_to_json(self):
        memo = MyMemo(
            memo="hello_memo",
            memo_type="memo_type",
            memo_format="png"
        )
        expected = '{"memo": "hello_memo", "memo_format": "png", "memo_type": "memo_type"}'
        result = memo.json()
        self.assertEqual(expected, result)

    def test_missing_optional_field(self):
        memo = MyMemo(
            memo="hello_memo",
            memo_format="png"
        )
        expected = '{"memo": "hello_memo", "memo_format": "png", "memo_type": null}'
        result = memo.json()
        self.assertEqual(expected, result)

    def test_missing_parameter(self):
        with self.assertRaises(ValidationError):
            MyMemo(
                memo_type="memo_type",
                memo_format="png"
            )

    def test_wrong_format(self):
        with self.assertRaises(ValidationError):
            MyMemo(
                memo="hello_memo",
                memo_type="memo_type",
                memo_format="exe"
            )
