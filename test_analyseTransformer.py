# coding=utf-8
from unittest import TestCase
from AnalyseTransformer import AnalyseTransformer


class TestAnalyseTransformer(TestCase):

    def test_replace_hash_with_format(self):
        # Arrange
        analyse_transformer = AnalyseTransformer()
        value_to_test = '1000 Der Standardwert für #0|@Value(fme_feature_type)#'
        expected_result = '1000 Der Standardwert für {0}'

        # Act
        # result = analyse_transformer.replace_hash_with_format(value_to_test, '#')
        result = analyse_transformer.replace_hash(value_to_test, '#')

        # Assert
        self.assertEqual(expected_result, result.get(value_to_test))

    def test_replace_hash_multiple(self):
        # Arrange
        analyse_transformer = AnalyseTransformer()
        value_to_test = '1000 Der Standardwert für #0|@Value(fme_feature_type)#.#1|$(GN_FIELD)# liegt nicht im Wertebereich #2|$(MIN_VALUE)#..#3|$(MAX_VALUE)#'
        expected_result = '1000 Der Standardwert für {0}.{1} liegt nicht im Wertebereich {2}..{3}'

        # Act
        # result = analyse_transformer.replace_hash_with_format(value_to_test, '#')
        result = analyse_transformer.replace_hash(value_to_test, '#')

        # Assert
        self.assertEqual(expected_result, result.get(value_to_test))
