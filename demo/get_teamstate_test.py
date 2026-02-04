from vaapi.client import Vaapi
import os


def get_logs():
    response = client.teamstate.list(
        log=2,
    )
    print(response[1])


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    get_logs()


"""
OUTPUT:

id=4192009 
frame=3167125 
representation_data={
    'players': [{
        'pose': {
            'rotation': 1.6189418151402306, 
            'translation': {
                'x': 1810.7993862768622, 
                'y': -2702.3230530795686}}, 
                'fallen': False, 
                'number': 3, 
                'ballAge': -1, 
                'robotRole': {
                    'roleStatic': 'role_midfielder_center', 
                    'roleDynamic': 'role_none'}, 
                'poseUpdate': '28594863', 
                'robotState': 'standby', 
                'timeToBall': 54613, 
                'wasStriker': False, 
                'readyToWalk': True, 
                'ballPosition': {
                    'x': 'Infinity', 
                    'y': 'Infinity'}, 
                'fallenUpdate': '28594863', 
                'ballAgeUpdate': '28594863', 
                'messageParsed': '28594847', 
                'robotRoleUpdate': '28594863', 
                'messageFrameInfo': {
                    'time': 283227, 
                    'frameNumber': 8305}, 
                'messageTimestamp': '28594863', 
                'robotStateUpdate': '28594863', 
                'timeToBallUpdate': '28594863', 
                'wantsToBeStriker': False, 
                'wasStrikerUpdate': '28594863', 
                'readyToWalkUpdate': '28594863', 
                'ballPositionUpdate': '28594863', 
                'wantsToBeStrikerUpdate': '28594863'}]} 
frame_number=8305


OUTPUT: should be
id=4839660 
frame=3675713 
representation_data={"players": 
    [{"pose": {
        "rotation": -0.028374726190361244, 
        "translation": {"x": -4003.922609005425, "y": -132.48037365459996}}, 
        "fallen": false, 
        "number": 1, 
        "ballAge": -1, 
        "robotRole": {
            "roleStatic": "role_unknown", 
            "roleDynamic": "role_none"}, 
        "poseUpdate": "1887342", 
        "robotState": "unstiff", 
        "timeToBall": 0, 
        "wasStriker": false, 
        "readyToWalk": false, 
        "ballPosition": {"x": 0.0, "y": 0.0}, 
        "fallenUpdate": "0", 
        "ballAgeUpdate": "0", 
        "messageParsed": "1887342", 
        "robotRoleUpdate": "0", 
        "messageFrameInfo": 
            {"time": 1034642, 
            "frameNumber": 30843}, 
        "messageTimestamp": "7451887", 
        "robotStateUpdate": "0", 
        "timeToBallUpdate": "0", 
        "wantsToBeStriker": false, 
        "wasStrikerUpdate": "1887342", 
        "readyToWalkUpdate": "0", 
        "ballPositionUpdate": "0", 
        "wantsToBeStrikerUpdate": "0"}, 
    {"pose": {"rotation": -0.18099283839604152, "translation": {"x": -2669.870942396079, "y": 324.6778866619525}}, "fallen": false, "number": 2, "ballAge": -1, "robotRole": {"roleStatic": "role_defender_left", "roleDynamic": "role_none"}, "ntpRequest": [{"sent": "3901256", "received": "0", "playerNum": 3}, {"sent": "7451887", "received": "0", "playerNum": 1}, {"sent": "3853197", "received": "0", "playerNum": 5}, {"sent": "1980862", "received": "0", "playerNum": 6}, {"sent": "18845547", "received": "0", "playerNum": 4}, {"sent": "16292633", "received": "0", "playerNum": 7}], "poseUpdate": "1932733", "robotState": "playing", "timeToBall": 56363, "wasStriker": false, "readyToWalk": true, "ballPosition": {"x": "Infinity", "y": "Infinity"}, "fallenUpdate": "1932733", "ballAgeUpdate": "1932733", "messageParsed": "1932717", "robotRoleUpdate": "1932733", "messageFrameInfo": {"time": 1080018, "frameNumber": 32202}, "messageTimestamp": "1932733", "ntpRequestUpdate": "1932733", "robotStateUpdate": "1932733", "timeToBallUpdate": "1932733", "wantsToBeStriker": false, "wasStrikerUpdate": "1932733", "readyToWalkUpdate": "1932733", "ballPositionUpdate": "1932733", "wantsToBeStrikerUpdate": "1932733"}, {"pose": {"rotation": -0.39809140747658567, "translation": {"x": -1136.5754523034113, "y": -401.0066646248127}}, "fallen": false, "number": 3, "ballAge": 33, "robotRole": {"roleStatic": "role_unknown", "roleDynamic": "role_none"}, "poseUpdate": "1878680", "robotState": "unstiff", "timeToBall": 0, "wasStriker": true, "readyToWalk": false, "ballPosition": {"x": 5424.591663949149, "y": 1811.9461820526076}, "fallenUpdate": "0", "ballAgeUpdate": "1878680", "messageParsed": "1878680", "robotRoleUpdate": "0", "messageFrameInfo": {"time": 1025980, "frameNumber": 30583}, "messageTimestamp": "3901256", "robotStateUpdate": "0", "timeToBallUpdate": "0", "wantsToBeStriker": false, "wasStrikerUpdate": "1878680", "readyToWalkUpdate": "0", "ballPositionUpdate": "1878680", "wantsToBeStrikerUpdate": "0"}, {"pose": {"rotation": 0.12183846126613367, "translation": {"x": 1953.085170076589, "y": 736.9689168568191}}, "fallen": false, "number": 4, "ballAge": 333, "robotRole": {"roleStatic": "role_unknown", "roleDynamic": "role_none"}, "poseUpdate": "1928286", "robotState": "unstiff", "timeToBall": 0, "wasStriker": true, "readyToWalk": false, "ballPosition": {"x": 318.8205869170164, "y": -52.40213478763071}, "fallenUpdate": "0", "ballAgeUpdate": "1928286", "messageParsed": "1928286", "robotRoleUpdate": "0", "messageFrameInfo": {"time": 1075587, "frameNumber": 32069}, "messageTimestamp": "18845547", "robotStateUpdate": "0", "timeToBallUpdate": "0", "wantsToBeStriker": false, "wasStrikerUpdate": "1928286", "readyToWalkUpdate": "0", "ballPositionUpdate": "1928286", "wantsToBeStrikerUpdate": "0"}, {"pose": {"rotation": 0.07901730404367502, "translation": {"x": -3068.7777812399013, "y": -650.9485285149465}}, "fallen": false, "number": 5, "ballAge": -1, "robotRole": {"roleStatic": "role_unknown", "roleDynamic": "role_none"}, "poseUpdate": "1838934", "robotState": "unstiff", "timeToBall": 0, "wasStriker": false, "readyToWalk": false, "ballPosition": {"x": 0.0, "y": 0.0}, "fallenUpdate": "0", "ballAgeUpdate": "0", "messageParsed": "1838934", "robotRoleUpdate": "0", "messageFrameInfo": {"time": 986235, "frameNumber": 29390}, "messageTimestamp": "3853197", "robotStateUpdate": "0", "timeToBallUpdate": "0", "wantsToBeStriker": false, "wasStrikerUpdate": "1838934", "readyToWalkUpdate": "0", "ballPositionUpdate": "0", "wantsToBeStrikerUpdate": "0"}, {"pose": {"rotation": 0.1020373702714022, "translation": {"x": -770.7114019025264, "y": -897.2484429342326}}, "fallen": false, "number": 6, "ballAge": 34, "robotRole": {"roleStatic": "role_unknown", "roleDynamic": "role_none"}, "poseUpdate": "1926487", "robotState": "unstiff", "timeToBall": 0, "wasStriker": true, "readyToWalk": false, "ballPosition": {"x": 675.8382495183583, "y": -78.557780766831}, "fallenUpdate": "0", "ballAgeUpdate": "1926487", "messageParsed": "1926487", "robotRoleUpdate": "0", "messageFrameInfo": {"time": 1073788, "frameNumber": 32015}, "messageTimestamp": "1980862", "robotStateUpdate": "0", "timeToBallUpdate": "0", "wantsToBeStriker": false, "wasStrikerUpdate": "1926487", "readyToWalkUpdate": "0", "ballPositionUpdate": "1926487", "wantsToBeStrikerUpdate": "0"}, {"pose": {"rotation": -0.23071819261315885, "translation": {"x": 2450.8748950353, "y": 482.5188033923641}}, "fallen": false, "number": 7, "ballAge": 0, "robotRole": {"roleStatic": "role_unknown", "roleDynamic": "role_none"}, "poseUpdate": "1930385", "robotState": "unstiff", "timeToBall": 0, "wasStriker": true, "readyToWalk": false, "ballPosition": {"x": 202.12902866904648, "y": -39.88206524370766}, "fallenUpdate": "0", "ballAgeUpdate": "1930385", "messageParsed": "1930385", "robotRoleUpdate": "0", "messageFrameInfo": {"time": 1077686, "frameNumber": 32132}, "messageTimestamp": "16292633", "robotStateUpdate": "0", "timeToBallUpdate": "0", "wantsToBeStriker": false, "wasStrikerUpdate": "1930385", "readyToWalkUpdate": "0", "ballPositionUpdate": "1930385", "wantsToBeStrikerUpdate": "0"}]}

"""


