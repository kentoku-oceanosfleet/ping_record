import subprocess
from datetime import datetime
import pytest
import re
from zoneinfo import ZoneInfo

def test_script_execution():
    """タイムスタンプスクリプトが正常に実行できることを確認"""
    result = subprocess.run(['./get_timestamp.sh'], capture_output=True, text=True)
    assert result.returncode == 0, "Script execution failed"
    assert result.stdout.strip(), "Script output should not be empty"

def test_timestamp_format():
    """出力がISO8601形式であることを確認"""
    result = subprocess.run(['./get_timestamp.sh'], capture_output=True, text=True)
    timestamp = result.stdout.strip()
    
    # ISO8601形式（YYYY-MM-DDThh:mm:ss+00:00）にマッチすることを確認
    iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$'
    assert re.match(iso8601_pattern, timestamp), f"Timestamp {timestamp} is not in ISO8601 format"
    
    # 各部分が適切な範囲内であることを確認
    dt = datetime.fromisoformat(timestamp)
    assert 1 <= dt.month <= 12, f"Invalid month: {dt.month}"
    assert 1 <= dt.day <= 31, f"Invalid day: {dt.day}"
    assert 0 <= dt.hour <= 23, f"Invalid hour: {dt.hour}"
    assert 0 <= dt.minute <= 59, f"Invalid minute: {dt.minute}"
    assert 0 <= dt.second <= 59, f"Invalid second: {dt.second}"

def test_timestamp_accuracy():
    """タイムスタンプが現在時刻に近い値であることを確認"""
    result = subprocess.run(['./get_timestamp.sh'], capture_output=True, text=True)
    timestamp = result.stdout.strip()
    
    script_time = datetime.fromisoformat(timestamp)
    current_time = datetime.now(ZoneInfo("UTC"))
    time_diff = abs((current_time - script_time).total_seconds())
    
    assert time_diff < 60, f"Timestamp difference {time_diff} seconds is too large (should be less than 60 seconds)"