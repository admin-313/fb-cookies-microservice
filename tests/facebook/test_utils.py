from src.facebook.utils import CookieStringParser

SAMPLE_COOKIE: str = (
    "datr=Iy-BV;ps_n=1;ps_l=1;sb=OoM;c_user=61765;b_user=611566;ar_debug=1;xs=6mP78as7M;fr=12apYWU2EK4zYl0;wd=1600x766;dpr=1.35;usida=eyU1MX0%3D;presence=EDF_7bCC;"
)


def test_parse_cookie_string_assertequals() -> None:
    expected_result: dict[str, str] = {
        "datr": "Iy-BV",
        "ps_n": "1",
        "ps_l": "1",
        "sb": "OoM",
        "c_user": "61765",
        "b_user": "611566",
        "ar_debug": "1",
        "xs": "6mP78as7M",
        "fr": "12apYWU2EK4zYl0",
        "wd": "1600x766",
        "dpr": "1.35",
        "usida": "eyU1MX0%3D",
        "presence": "EDF_7bCC",
    }
    real_result: dict[str, str] = CookieStringParser.parse_cookie_string(SAMPLE_COOKIE)

    assert real_result == expected_result