import subprocess
from datetime import datetime
import pytest
import re
from zoneinfo import ZoneInfo
import json

def test_script_execution():
    """タイムスタンプスクリプトが正常に実行できることを確認"""
    result = subprocess.run(['./get_timestamp.sh'], capture_output=True, text=True)
    assert result.returncode == 0, "スクリプトの実行に失敗しました"
    assert result.stdout.strip(), "スクリプトの出力が空です"

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

def test_ping_no_args():
    """引数なしでの実行時にエラーメッセージが表示されることを確認"""
    result = subprocess.run(['./get_ping.sh'], capture_output=True, text=True)
    assert result.returncode == 1, "引数なしの場合はエラーを返す必要があります"
    assert "Usage:" in result.stderr + result.stdout, "使用方法のメッセージが表示されていません"

def test_ping_execution():
    """pingスクリプトが正常に実行でき、JSON形式で出力されることを確認"""
    test_ip = "8.8.8.8"
    result = subprocess.run(['./get_ping.sh', test_ip], capture_output=True, text=True)
    assert result.returncode == 0, "pingスクリプトの実行に失敗しました"
    assert result.stdout.strip(), "スクリプトの出力が空です"
    
    # シングルクォートをダブルクォートに変換してJSON解析
    output_json = result.stdout.strip().replace("'", '"')
    try:
        data = json.loads(output_json)
    except json.JSONDecodeError:
        pytest.fail("出力が正しいJSON形式ではありません")

def test_ping_output_format():
    """ping結果の出力形式と値の妥当性を確認"""
    test_ip = "8.8.8.8"
    result = subprocess.run(['./get_ping.sh', test_ip], capture_output=True, text=True)
    output_json = result.stdout.strip().replace("'", '"')
    data = json.loads(output_json)
    
    # 必要なフィールドが存在することを確認
    assert 'dst' in data, "出力にdstフィールドが含まれていません"
    assert 'response_ms' in data, "出力にresponse_msフィールドが含まれていません"
    
    # 値の妥当性チェック
    assert data['dst'] == test_ip, f"宛先IP {data['dst']} が入力値 {test_ip} と一致しません"
    assert isinstance(data['response_ms'], (int, float)), "応答時間は数値である必要があります"
    assert 0 <= float(data['response_ms']) <= 1000, "応答時間が異常です（0-1000ms の範囲外）"