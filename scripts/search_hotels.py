#!/usr/bin/env python3
"""
onezion-hotel-flights: 统一酒店搜索脚本
支持 AIGoHotel MCP 和高德地图 API
"""
import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# 加载 .env
ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(ENV_FILE):
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

def search_amap_poi(keyword, city="深圳"):
    """高德地图 POI 搜索（辅助定位）"""
    api_key = os.environ.get('AMAP_API_KEY', '')
    if not api_key:
        return {"error": "AMAP_API_KEY not set"}
    
    params = urllib.parse.urlencode({
        'key': api_key,
        'keywords': keyword,
        'city': city,
        'offset': 5,
        'page': 1,
        'extensions': 'all'
    })
    url = f"https://restapi.amap.com/v3/place/text?{params}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}

def search_aigohotel(place, checkin=None, stay_nights=1, star_min=3, star_max=5, size=5):
    """AIGoHotel 酒店搜索"""
    api_key = os.environ.get('AIGOHOTEL_API_KEY', '')
    if not api_key:
        return {"error": "AIGOHOTEL_API_KEY not set. Apply at https://mcp.agentichotel.cn/apply"}
    
    if not checkin:
        checkin = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    payload = json.dumps({
        "place": place,
        "checkIn": checkin,
        "stayNights": stay_nights,
        "starRatings": [star_min, star_max],
        "size": size,
        "withHotelAmenities": True,
        "withRoomAmenities": False
    }).encode()
    
    req = urllib.request.Request(
        "https://mcp.aigohotel.com/api/find-hotels",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: search_hotels.py <place> [checkin] [stay_nights] [star_min] [star_max]")
        print("Example: search_hotels.py '深圳龙岗宝龙地铁站' 2026-05-04 1 4 5")
        sys.exit(1)
    
    place = sys.argv[1]
    checkin = sys.argv[2] if len(sys.argv) > 2 else None
    stay_nights = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    star_min = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    star_max = int(sys.argv[5]) if len(sys.argv) > 5 else 5
    
    print(f"🔍 搜索: {place}")
    print(f"📅 入住: {checkin or '明天'} | 晚数: {stay_nights} | 星级: {star_min}-{star_max}星")
    print("-" * 60)
    
    result = search_aigohotel(place, checkin, stay_nights, star_min, star_max)
    
    if "error" in result:
        print(f"❌ 错误: {result['error']}")
    elif isinstance(result, list):
        for i, hotel in enumerate(result, 1):
            name = hotel.get('Name', '未知')
            price = hotel.get('Price', 'N/A')
            currency = hotel.get('Currency', 'CNY')
            star = hotel.get('StarRating', '?')
            address = hotel.get('Address', '')
            distance = hotel.get('DistanceInMeters', '')
            amenities = hotel.get('HotelAmenities', [])
            
            print(f"{i}. {name}")
            print(f"   💰 {currency} {price} | ⭐ {star}星")
            print(f"   📍 {address}")
            if distance:
                print(f"   📏 距离: {distance}m")
            if amenities:
                print(f"   🏊 设施: {', '.join(amenities[:5])}")
            print()
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
