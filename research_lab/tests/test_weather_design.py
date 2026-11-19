import tempfile
import unittest
from pathlib import Path

import numpy as np

from research_lab import weather_design as weather


class WeatherDesignTests(unittest.TestCase):
    def test_spline_reproduces_left_boundary_cubic_and_rejects_quadratic(self):
        # A piecewise cubic with zero boundary curvature and three internal
        # quarter knots. The historical quadratic-padded construction fails
        # this reproduction test even though its matrix has the same rank.
        x = np.linspace(0, 1, 49)
        spline = np.column_stack((np.ones(x.size), weather.natural_spline(x)))
        natural_curve = (
            x**3 - 3 * np.maximum(x - 0.25, 0)**3
            + 3 * np.maximum(x - 0.5, 0)**3 - np.maximum(x - 0.75, 0)**3
        )
        matrix = np.column_stack((natural_curve, x**2))
        fitted = spline @ np.linalg.lstsq(spline, matrix, rcond=None)[0]
        np.testing.assert_allclose(fitted[:, 0], natural_curve, atol=1e-12)
        self.assertGreater(np.max(np.abs(fitted[:, 1] - x**2)), 0.001)

    def test_all_registered_calendars_against_scipy_interpolation(self):
        # References from scipy.interpolate.CubicSpline(knots, (-1)**arange,
        # bc_type="natural") evaluated at the seven probe indices below.
        # Fixed fixtures keep SciPy out of the sandbox runtime dependencies.
        expected = {
            3: [0.9166875, 0.344, -0.248, -0.859375, 0.328125, 0.876, -0.7505625],
            4: [0.885767195767, 0.112804232804, -0.611851851852, 0.107142857143,
                0.871693121693, -1.038518518519, 0.658571428571],
            6: [0.827105769231, -0.291076923077, -1.020923076923, 0.655048076923,
                -0.698317307692, -0.140923076923, 0.485701923077],
            8: [0.769505918289, -0.625340969836, -0.919609011073, -1.0,
                0.486063382971, 0.941889270714, 0.318927835052],
        }
        x = np.arange(121)
        for df, reference in expected.items():
            with self.subTest(df=df):
                basis = np.column_stack((np.ones(x.size), weather.natural_spline(x, df)))
                knots = np.arange(0, 121, 120 // df)
                coef = np.linalg.solve(basis[knots], (-1.0) ** np.arange(df + 1))
                np.testing.assert_allclose(basis[[1, 8, 16, 45, 65, 92, 117]] @ coef,
                                           reference, atol=1e-10, rtol=0)

    def test_fixed_windows_remove_month_and_calendar_trend(self):
        for years in (11, 7, 4):
            month = np.tile(np.arange(1, 13), years)
            trend = np.arange(12 * years) / 10
            seasonal_series = np.sin(2 * np.pi * month / 12) + trend
            residuals = weather._adjust(month, seasonal_series)
            np.testing.assert_allclose(residuals, 0, atol=1e-12)

    def test_measurement_scale_and_concentration(self):
        dates = ["2000-01", "2000-02", "2000-03", "2000-04"]
        series = np.array([2., 8., 8., 2.])
        residuals = np.array([-2., 2., 0., 0.])
        result = weather._summary("fixture", "cold_days", dates, series, residuals)
        self.assertEqual(result["reporting_increment"], 5)
        self.assertEqual(result["raw_ss"], 36)
        self.assertEqual(result["residual_ss"], 8)
        self.assertEqual(result["months_for_half_ss"], 1)
        self.assertEqual(result["top_month"], dates[0])
        self.assertAlmostEqual(result["residual_share"], 8 / 36)
        self.assertEqual(result["largest_month_share"], 0.5)

    def test_invalid_calendar_and_benchmark_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "one HKO row"):
            weather._weather_matrix([])
        x = np.arange(1, 121).reshape(20, 6)
        with self.assertRaisesRegex(ValueError, "benchmark failed"):
            weather._check_r_reference([], x, x)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / weather.CLIMATE
            path.parent.mkdir(parents=True)
            path.write_text("unreviewed source revision\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Unrecognised source revision"):
                weather.analyze(root)
            for degrees in ((), (4, 4), (5,), (4.0,), (True,)):
                with self.subTest(degrees=degrees), self.assertRaises(ValueError):
                    weather.design_grid(root, degrees)


if __name__ == "__main__":
    unittest.main()
