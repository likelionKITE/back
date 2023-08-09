import time

import django as django
import requests
from django.core.management.base import BaseCommand

#
from KITE_back import settings
import main.models
from festival.models import DetailIntroFest
from main.models import ServiceCode, AreaCode, Tour, DetailCommon, DetailInfo
from travel.models import DetailIntroTravel


class Command(BaseCommand):
    help = 'API 데이터를 DB에 저장'

    def handle(self, *args, **options):
        service_key = [settings.api_key_ja, settings.api_key_sy, settings.api_key_jy]
        api_key = service_key[0]
        api_url_base = "http://apis.data.go.kr/B551011/EngService1"
        params = "?MobileOS=ETC&MobileApp=KITE&numOfRows=50000&_type=json&serviceKey="

        # # save servicecode
        contenttypeid = [76, 85]

        # for type in contenttypeid:
        #     api_url = api_url_base + "/categoryCode1" + params + api_key + f"&contentTypeId={type}"
        #     res = requests.get(api_url)
        #     print(res, api_url)
        #     cat1s = res.json()['response']['body']['items']['item']
        #
        #     cat1_code = []
        #     cat1_name = []
        #
        #     for i in cat1s:
        #         cat1_code.append(i['code'])
        #         cat1_name.append(i['name'])
        #
        #     for cat1_idx in range(len(cat1_code)):
        #         cat2_code = []
        #         cat2_name = []
        #         api_url = api_url_base + "/categoryCode1" + params + api_key + f"&contentTypeId={type}&cat1={cat1_code[cat1_idx]}"
        #         res = requests.get(api_url)
        #         print(res, api_url)
        #         cat2s = res.json()['response']['body']['items']['item']
        #
        #         for j in cat2s:
        #             cat2_code.append(j['code'])
        #             cat2_name.append(j['name'])
        #
        #         for cat2_idx in range(len(cat2_code)):
        #             api_url = api_url_base + "/categoryCode1" + params + api_key + f"&contentTypeId={type}&cat1={cat1_code[cat1_idx]}&cat2={cat2_code[cat2_idx]}"
        #             res = requests.get(api_url)
        #             print(res, api_url)
        #             cat3s = res.json()['response']['body']['items']['item']
        #
        #             for k in cat3s:
        #                 servicecode_data = ServiceCode()
        #                 try:
        #                     ServiceCode.objects.get(sub_code=k['code'])
        #                 except:
        #                     servicecode_data.content_type_id = str(type)
        #                     servicecode_data.main_code = cat1_code[cat1_idx]
        #                     servicecode_data.main_name = cat1_name[cat1_idx]
        #                     servicecode_data.mid_code = cat2_code[cat2_idx]
        #                     servicecode_data.mid_name = cat2_name[cat2_idx]
        #                     servicecode_data.sub_code = k['code']
        #                     servicecode_data.sub_name = k['name']
        #                     servicecode_data.save()

        #
        #
        # # save areacode
        # api_url = api_url_base + "/areaCode1" + params + api_key
        # res = requests.get(api_url)
        # print(res, res.text, api_url)
        # areacodes = res.json()['response']['body']['items']['item']
        #
        # area_code = []
        # area_name = []
        #
        # for i in areacodes:
        #     area_code.append(i['code'])
        #     area_name.append(i['name'])
        #
        # for area_idx in range(len(area_code)):
        #     api_url = api_url_base + "/areaCode1" + params + api_key + f"&areaCode={area_code[area_idx]}"
        #     res = requests.get(api_url)
        #     print(res, res.text, api_url)
        #     sigungus = res.json()['response']['body']['items']['item']
        #
        #     for j in sigungus:
        #         areacode_data = AreaCode()
        #         try:
        #             AreaCode.objects.get(code=area_code[area_idx], sigungu_code=j['code'])
        #         except:
        #             areacode_data.code = area_code[area_idx]
        #             areacode_data.name = area_name[area_idx]
        #             areacode_data.sigungu_code = j['code']
        #             areacode_data.sigungu_name = j['name']
        #             areacode_data.save()
        #
        #
        # save tour
        cnt = 0
        idx = 0
        for typeid in contenttypeid:
            # save tour-travel
            api_url = api_url_base + "/areaBasedList1" + params + api_key + f"&contentTypeId={typeid}&listYN=Y&arrange=A"
            res = requests.get(api_url)
            print(res, api_url)
            tours = res.json()['response']['body']['items']['item']

            for i in tours:
                cnt += 1
                if cnt > 870:
                    cnt = 0
                    idx += 1
                    api_key = service_key[idx]
                tour_data = Tour()
                print(i)
                try:
                    Tour.objects.get(content_id=i['contentid'])
                except:
                    try: # 소분류가 이상하게 된 게 있어서,,(관광지;76인데 카테고리는 78 등등 그거 제외하고 저장)
                        tour_data.addr1 = i['addr1']
                        tour_data.addr2 = i['addr2']
                        tour_data.area_code = i['areacode']
                        tour_data.sigungu_code = AreaCode.objects.get(code=i['areacode'], sigungu_code=i['sigungucode'])
                        tour_data.cat1 = i['cat1']
                        tour_data.cat2 = i['cat2']
                        tour_data.cat3 = ServiceCode.objects.get(sub_code=i['cat3'])
                        tour_data.content_id = i['contentid']
                        tour_data.content_type_id = i['contenttypeid']
                        tour_data.first_image = i['firstimage']
                        tour_data.first_image2 = i['firstimage2']
                        tour_data.cpyrhtDivCd = i['cpyrhtDivCd']
                        tour_data.mapx = i['mapx']
                        tour_data.mapy = i['mapy']
                        tour_data.mlevel = i['mlevel']
                        tour_data.modified_time = i['modifiedtime']
                        tour_data.tel = i['tel']
                        tour_data.title = i['title']
                        tour_data.save()

                        # 상세페이지 정보
                        ## save detailcommon
                        api_url = api_url_base + "/detailCommon1" + params + api_key + f"&contentId={i['contentid']}&defaultYN=Y&overviewYN=Y&transGuideYN=Y"
                        time.sleep(0.5)
                        res = requests.get(api_url)
                        print(res, res.text, api_url)
                        commons = res.json()['response']['body']['items']['item']
                        common_data = DetailCommon()
                        for common in commons:
                            try:
                                DetailCommon.objects.get(content_id=Tour.objects.get(content_id=common['contentid']))
                            except:
                                common_data.overview = common['overview']
                                common_data.tel_Name = common['telname']
                                common_data.title = common['title']
                                common_data.modified_time = common['modifiedtime']
                                common_data.homepage = common['homepage']
                                common_data.content_id = Tour.objects.get(content_id=common['contentid'])
                                common_data.save()

                        ## save detailinfo
                        api_url = api_url_base + "/detailInfo1" + params + api_key + f"&contentId={i['contentid']}&contentTypeId={i['contenttypeid']}"
                        time.sleep(0.5)
                        res = requests.get(api_url)
                        print(res, res.text, api_url)
                        try:  # 아예 detailinfo가 없는 게 있음
                            infos = res.json()['response']['body']['items']['item']
                            info_data = DetailInfo()
                            for info in infos:
                                try:
                                    DetailInfo.objects.get(content_id=Tour.objects.get(content_id=common['contentid']))
                                except:
                                    info_data.info_name = info['infoname']
                                    info_data.info_text = info['infotext']
                                    info_data.fidgubun = info['fidgubun']
                                    info_data.content_id = Tour.objects.get(content_id=info['contentid'])
                                    info_data.content_type_id = info['contenttypeid']
                                    info_data.serial_num = info['serialnum']
                                    info_data.save()
                        except:  # 그럴 경우 contentid만 명시하고 나머지 필드 다 비운 채로 저장
                            info_data = DetailInfo()
                            info_data.content_id = Tour.objects.get(content_id=i['contentid'])
                            info_data.save()

                        ## save detailintro
                        api_url = api_url_base + "/detailIntro1" + params + api_key + f"&contentId={i['contentid']}&contentTypeId={i['contenttypeid']}"
                        time.sleep(0.5)
                        res = requests.get(api_url)
                        print(res, res.text, api_url)
                        intros = res.json()['response']['body']['items']['item']

                        if typeid == 76:
                            intro_data = DetailIntroTravel()

                            for intro in intros:
                                try:
                                    DetailIntroTravel.objects.get(content_id=Tour.objects.get(content_id=common['contentid']))
                                except:
                                    intro_data.content_id = Tour.objects.get(content_id=intro['contentid'])
                                    intro_data.heritage1 = intro['heritage1']
                                    intro_data.accom_count = intro['accomcount']
                                    intro_data.exp_age_range = intro['expagerange']
                                    intro_data.exp_guide = intro['expguide']
                                    intro_data.info_center = intro['infocenter']
                                    intro_data.open_date = intro['opendate']
                                    intro_data.parking = intro['parking']
                                    intro_data.rest_date = intro['restdate']
                                    intro_data.use_season = intro['useseason']
                                    intro_data.use_time = intro['usetime']
                                    intro_data.save()
                        else:
                            intro_data = DetailIntroFest()

                            for intro in intros:
                                try:
                                    DetailIntroFest.objects.get(content_id=Tour.objects.get(content_id=common['contentid']))
                                except:
                                    intro_data.content_id = Tour.objects.get(content_id=intro['contentid'])
                                    intro_data.place_info = intro['placeinfo']
                                    intro_data.event_homepage = intro['eventhomepage']
                                    intro_data.event_place = intro['eventplace']
                                    intro_data.play_time = intro['playtime']
                                    intro_data.program = intro['program']
                                    intro_data.age_limit = intro['agelimit']
                                    intro_data.spend_time_festival = intro['spendtimefestival']
                                    intro_data.booking_place = intro['bookingplace']
                                    intro_data.discount_info_festival = intro['discountinfofestival']
                                    intro_data.event_start_date = intro['eventstartdate']
                                    intro_data.event_end_date = intro['eventenddate']
                                    intro_data.sponsor1 = intro['sponsor1']
                                    intro_data.sponsor1tel = intro['sponsor1tel']
                                    intro_data.sponsor2 = intro['sponsor2']
                                    intro_data.sponsor2tel = intro['sponsor2tel']
                                    intro_data.sub_event = intro['subevent']
                                    intro_data.use_time_festival = intro['usetimefestival']
                                    intro_data.save()




                    except main.models.ServiceCode.DoesNotExist as e:
                        print('contentid: '+i['contentid']+', contenttypeid: '+i['contenttypeid']+', cat: '+i['cat3'])
                        print(e)
                    except main.models.AreaCode.DoesNotExist as e:
                        print('contentid: '+i['contentid']+', contenttypeid: '+i['contenttypeid']+', areacode: '+i['areacode'])
                        print(e)
                    except requests.exceptions.JSONDecodeError as e:
                        print(e)



