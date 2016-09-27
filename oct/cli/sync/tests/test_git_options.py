# coding=utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from click import UsageError
from oct.cli.sync.git_options import git_version_specifier, validate_git_specifier


class ValidateGitSpecifierTestCase(TestCase):
    def test_commit(self):
        self.assertEqual(validate_git_specifier(refspec=None, branch=None, commit='SHA', tag=None), None)

    def test_commit_and_anything(self):
        with self.assertRaisesRegexp(UsageError, 'neither a refspec, branch, or tag'):
            validate_git_specifier(refspec='pulls/1/head', branch=None, commit='SHA', tag=None)
        with self.assertRaisesRegexp(UsageError, 'neither a refspec, branch, or tag'):
            validate_git_specifier(refspec=None, branch='master', commit='SHA', tag=None)
        with self.assertRaisesRegexp(UsageError, 'neither a refspec, branch, or tag'):
            validate_git_specifier(refspec=None, branch=None, commit='SHA', tag='v1.0.0')

    def test_tag(self):
        self.assertEqual(validate_git_specifier(refspec=None, branch=None, commit=None, tag='v1.0.0'), None)

    def test_tag_and_anything(self):
        with self.assertRaisesRegexp(UsageError, 'neither a refspec, branch, or commit'):
            validate_git_specifier(refspec='pulls/1/head', branch=None, commit=None, tag='v1.0.0')
        with self.assertRaisesRegexp(UsageError, 'neither a refspec, branch, or commit'):
            validate_git_specifier(refspec=None, branch='master', commit=None, tag='v1.0.0')
        with self.assertRaises(UsageError):  # the commit check aliases this, so we don't check the content
            validate_git_specifier(refspec=None, branch=None, commit='SHA', tag='v1.0.0')

    def test_branch(self):
        self.assertEqual(validate_git_specifier(refspec=None, branch='master', commit=None, tag=None), None)

    def test_branch_and_anything(self):
        with self.assertRaises(UsageError):  # the commit check aliases this, so we don't check the content
            validate_git_specifier(refspec=None, branch='master', commit='SHA', tag=None)
        with self.assertRaises(UsageError):  # the branch check aliases this, so we don't check the content
            validate_git_specifier(refspec=None, branch='master', commit=None, tag='v1.0.0')

    def test_refspec(self):
        with self.assertRaisesRegexp(UsageError, 'the name of the branch to create for it is required'):
            validate_git_specifier(refspec='pulls/1/head', branch=None, commit=None, tag=None)

    def test_refspec_master_branch(self):
        with self.assertRaisesRegexp(UsageError, 'cannot be the master branch'):
            validate_git_specifier(refspec='pulls/1/head', branch='master', commit=None, tag=None)

    def test_refspec_branch(self):
        self.assertEqual(validate_git_specifier(refspec='pulls/1/head', branch='myfeature', commit=None, tag=None), None)

    def test_refspec_and_anything(self):
        with self.assertRaises(UsageError):  # the commit check aliases this, so we don't check the content
            validate_git_specifier(refspec='pulls/1/head', branch=None, commit='SHA', tag=None)
        with self.assertRaises(UsageError):  # the branch check aliases this, so we don't check the content
            validate_git_specifier(refspec='pulls/1/head', branch=None, commit=None, tag='v1.0.0')


class GitVersionSpecifierTestCase(TestCase):
    def test_commit(self):
        self.assertEqual(
            git_version_specifier(refspec=None, branch=None, commit='SHA', tag=None),
            {'origin_ci_sync_version': 'SHA'}
        )

    def test_tag(self):
        self.assertEqual(
            git_version_specifier(refspec=None, branch=None, commit=None, tag='v1.0.0'),
            {'origin_ci_sync_version': 'v1.0.0'}
        )

    def test_branch(self):
        self.assertEqual(
            git_version_specifier(refspec=None, branch='master', commit=None, tag=None),
            {'origin_ci_sync_version': 'master'}
        )

    def test_refspec_branch(self):
        self.assertEqual(
            git_version_specifier(refspec='pulls/1/head', branch='myfeature', commit=None, tag=None),
            {
                'origin_ci_sync_refspec': 'pulls/1/head:myfeature',
                'origin_ci_sync_version': 'myfeature'
            }
        )
