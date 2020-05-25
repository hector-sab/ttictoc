import sys
import os

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MODULE_DIR + "/../")

from statistics import mean
import pytest

import time
from ttictoc.tictoc import TimerError
from ttictoc import Timer, tic, toc, tic2, toc2
from ttictoc.tictoc import (
    _TICTOC_HELPER_CLASS_5da0381c_27af_4d67_8881,
    _TICTOC_HELPER_CLASS_b178dbeb_a38c_4c13_8b0d,
)


class TestMatlabLike:
    def test_tictoc(self):
        """Test simple cases"""
        tic()
        delta_gt = 0.5
        time.sleep(delta_gt)
        elapsed = toc()
        diff = abs(delta_gt - elapsed)
        assert diff < 0.01, (
            f"Diff is too big. Expected diff: {0.01}" ", obtained diff {diff}"
        )

    def test_buffer(self):
        """Test number of elements in the buffer"""
        num_iters = 20
        for _ in range(num_iters):
            tic()

        num_tics = len(
            _TICTOC_HELPER_CLASS_5da0381c_27af_4d67_8881._timers_start
        )

        assert num_tics == num_iters, "Invlid number of tics in buffer"

    def test_buffer_values(self):
        """Test values collected in nesting"""
        num_iters = 10
        delta_gt = 0.5
        values = []
        tic()
        time.sleep(delta_gt)
        elapsed = toc()
        values.append(elapsed)
        for _ in range(num_iters):
            tic()
            time.sleep(delta_gt)
            elapsed = toc()
            values.append(elapsed)

        delta = mean(values)
        diff = abs(delta_gt - delta)

        assert diff < 0.01, (
            "Diff is too big. Expected diff: 0.01"
            ", obtained diff {}".format(diff)
        )


class TestNonMatlabLike:
    def test_tictoc(self):
        """Test simple cases"""
        tic2()
        delta_gt = 0.5
        time.sleep(delta_gt)
        elapsed = toc2()
        diff = abs(delta_gt - elapsed)
        assert diff < 0.01, (
            "Diff is too big. Expected diff: 0.01"
            ", obtained diff {}".format(diff)
        )

    def test_restart_type(self):
        """Test the variable"""
        num_iters = 10
        for _ in range(num_iters):
            tic2()

        _start_time = _TICTOC_HELPER_CLASS_b178dbeb_a38c_4c13_8b0d._start_time
        assert isinstance(_start_time, float), (
            "Invalid starting time variable type."
            "Expected type: float, obtained type: {}".format(_start_time)
        )

    def test_restart(self):
        """Test number of elements in the buffer"""
        num_iters = 10
        delta_gt = 0.5
        for _ in range(num_iters):
            tic2()
            time.sleep(delta_gt - 0.2)

        tic2()
        time.sleep(delta_gt)
        elapsed = toc2()

        diff = abs(elapsed - delta_gt)

        assert diff < 0.01, (
            "Diff is too big. Expected diff: 0.01"
            ", obtained diff {}".format(diff)
        )

    def test_buffer_values(self):
        """Test values collected in nesting"""
        num_iters = 10
        delta_gt = 0.5

        tic2("init")
        time.sleep(delta_gt)

        for i in range(num_iters):
            tic2(i)
            time.sleep(delta_gt)
            toc2(i)

        toc2("init")

        delta = []
        for i in range(num_iters):
            val = _TICTOC_HELPER_CLASS_b178dbeb_a38c_4c13_8b0d.elapsed[i]
            delta.append(val)

        delta = mean(delta)
        diff1 = abs(delta_gt - delta)

        delta = _TICTOC_HELPER_CLASS_b178dbeb_a38c_4c13_8b0d.elapsed["init"]
        diff2 = abs(delta_gt * (num_iters + 1) - delta)

        assert diff1 < 0.01 and diff2 < 0.01, (
            "Diff is too big. Diffs of {} and {}".format(diff1, diff2)
        )


class TestTimer:
    def test_clear_timers(self):
        """Test clear timers"""
        t = Timer(matlab_like=False)
        for i in range(10):
            t.start(i)

        t.clear_timers()
        assert len(t._timers_start) == 0, "Timers not restarting"

    def test_error_not_initialized(self):
        """Test the error when timer has been not initialized"""
        t = Timer(matlab_like=True)

        with pytest.raises(TimerError):
            assert t.stop()

    def test_error_not_initialized_non_matlab_like(self):
        """Test the error when timer has been not initialized"""
        t = Timer(matlab_like=False)

        with pytest.raises(TimerError):
            assert t.stop()

    def test_error_not_initialized_non_matlab_like_key(self):
        """Test the error when timer has been not initialized"""
        t = Timer(matlab_like=False)

        with pytest.raises(TimerError):
            assert t.stop("init")


# TODO:  Test tic,toc nested

# TODO: Test Time class simple and nested
