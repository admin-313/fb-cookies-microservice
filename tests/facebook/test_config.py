import pytest
from src.facebook.config import GetJSONConfig
from src.facebook.schemas import JSONFBWebdriverConfig
from pydantic import ValidationError

def test_get_json_config_returns_config_data() -> None:
    expected_result: dict[str, str] = {
        "proxy": "socks5://example.com",
        "user_agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0 [ip:36.2.64.67]",
        "cookie": "datr=Iy-BV;ps_n=1;ps_l=1;sb=OoM;c_user=61765;b_user=611566;ar_debug=1;xs=6mP78as7M;fr=12apYWU2EK4zYl0;wd=1600x766;dpr=1.35;usida=eyU1MX0%3D;presence=EDF_7bCC;",
        "adsmanager_link": "https://dummyinfo.hu"
    }

    real_result: JSONFBWebdriverConfig = GetJSONConfig.get_json_config("./tests/test.config.json")

    assert real_result.model_dump() == expected_result

def test_get_json_config_throws_FBWebdriverInvalidConfigProvided() -> None:
    with pytest.raises(ValidationError) as conf_error:
        GetJSONConfig.get_json_config("./tests/test.broken_config.json")
    
    assert conf_error.type is ValidationError