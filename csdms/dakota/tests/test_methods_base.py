#!/usr/bin/env python
#
# Tests for dakota.methods.base module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import raises, assert_true, assert_is_none, assert_equal
from csdms.dakota.methods.base import MethodsBase
from . import start_dir, data_dir

# Helpers --------------------------------------------------------------


class Concrete(MethodsBase):

    """A subclass of MethodsBase used for testing."""

    def __init__(self):
        MethodsBase.__init__(self)
        self.variables = ['x0', 'x1']

    def method_block(self):
        return MethodsBase.method_block(self)

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = Concrete()


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


@raises(TypeError)
def test_instantiate():
    """Test whether MethodsBase fails to instantiate."""
    d = MethodsBase()


def test_get_run_directory():
    """Test getting the run_directory property."""
    assert_equal(c.run_directory, os.getcwd())


def test_set_run_directory():
    """Test setting the run_directory property."""
    run_dir = '/foo/bar'
    c.run_directory = run_dir
    assert_equal(c.run_directory, run_dir)


def test_get_template_file():
    """Test getting the template_file property."""
    assert_is_none(c.template_file)


def test_set_template_file():
    """Test setting the template_file property."""
    template_file = 'foo.tmpl'
    c.template_file = template_file
    assert_equal(os.path.basename(c.template_file), template_file)


def test_get_input_files():
    """Test getting the input_files property."""
    assert_equal(c.input_files, tuple())


def test_set_input_files():
    """Test setting the input_files property."""
    for input_file in ['foo.in', ['foo.in'], ('foo.in',)]:
        c.input_files = input_file
        if type(input_file) is not str:
            input_file = input_file[0]
        pathified_input_file = os.path.abspath(input_file)
        assert_equal(c.input_files, (pathified_input_file,))


@raises(TypeError)
def test_set_input_files_fails_if_scalar():
    """Test that the input_files property fails with a non-string scalar."""
    input_file = 42
    c.input_files = input_file


def test_get_variables():
    """Test getting the variables property."""
    assert_true(type(c.variables) is list)


def test_set_variables():
    """Test setting the variables property."""
    for desc in [['x1'], ('x1',)]:
        c.variables = desc
        assert_equal(c.variables, desc)


@raises(TypeError)
def test_set_variables_fails_if_scalar():
    """Test that the variables property fails with scalar string."""
    desc = 'x1'
    c.variables = desc


def test_get_responses():
    """Test getting the responses property."""
    assert_equal(c.responses, tuple())


def test_set_responses():
    """Test setting the responses property."""
    for desc in [['Qs_median'], ('Qs_median',)]:
        c.responses = desc
        assert_equal(c.responses, desc)


@raises(TypeError)
def test_set_responses_fails_if_scalar():
    """Test that the responses property fails with scalar string."""
    desc = 'Qs_median'
    c.responses = desc


def test_get_response_files():
    """Test getting the response_files property."""
    assert_equal(c.response_files, tuple())


def test_set_response_files():
    """Test setting the response_files property."""
    for files in [['HYDROASCII.QS'], ('HYDROASCII.QS',)]:
        c.response_files = files
        assert_equal(c.response_files, files)


@raises(TypeError)
def test_set_response_files_fails_if_scalar():
    """Test that the response_files property fails with scalar string."""
    files = 'HYDROASCII.QS'
    c.response_files = files


def test_get_response_statistics():
    """Test getting the response_statistics property."""
    assert_equal(c.response_statistics, tuple())


def test_set_response_statistics():
    """Test setting the response_statistics property."""
    for stats in [['median'], ('median',)]:
        c.response_statistics = stats
        assert_equal(c.response_statistics, stats)


@raises(TypeError)
def test_set_response_statistics_fails_if_scalar():
    """Test that the response_statistics property fails with scalar string."""
    stats = 'median'
    c.response_statistics = stats


def test_environment_block():
    """Test type of environment_block method results."""
    s = c.environment_block()
    assert_true(type(s) is str)


def test_method_block():
    """Test type of method_block method results."""
    s = c.method_block()
    assert_true(type(s) is str)


def test_variables_block():
    """Test type of variables_block method results."""
    s = c.variables_block()
    assert_true(type(s) is str)


def test_interface_block():
    """Test type of interface_block method results."""
    s = c.interface_block()
    assert_true(type(s) is str)


def test_responses_block():
    """Test type of responses_block method results."""
    s = c.responses_block()
    assert_true(type(s) is str)


def test_responses_block_with_objective_function():
    """Test type of responses_block method results."""
    c.is_objective_function = True
    s = c.responses_block()
    assert_true(type(s) is str)
