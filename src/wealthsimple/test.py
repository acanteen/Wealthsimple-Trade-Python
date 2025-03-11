import requests
import json

url = "https://my.wealthsimple.com/graphql"

payload = json.dumps({
  "operationName": "FetchActivityFeedItems",
  "variables": {
    "orderBy": "OCCURRED_AT_DESC",
    "condition": {
      "accountIds": [
        "fhsa-JUV5mp1Rgw",
        "fhsa-_zc24xmi0w",
        "non-registered-9k899x_o",
        "non-registered-HKXypwaspQ",
        "non-registered-jgxi45op",
        "rrsp-emrajkgf",
        "rrsp-qmoat6_o",
        "tfsa-8aqbjxvf",
        "tfsa-a8kdbbgy"
      ],
      "endDate": "2024-11-22"
    },
    "first": 10000
  },
  "query": "query FetchActivityFeedItems($first: Int, $cursor: Cursor, $condition: ActivityCondition, $orderBy: [ActivitiesOrderBy!] = OCCURRED_AT_DESC) {\n  activityFeedItems(\n    first: $first\n    after: $cursor\n    condition: $condition\n    orderBy: $orderBy\n  ) {\n    edges {\n      node {\n        ...Activity\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Activity on ActivityFeedItem {\n  accountId\n  aftOriginatorName\n  aftTransactionCategory\n  aftTransactionType\n  amount\n  amountSign\n  assetQuantity\n  assetSymbol\n  canonicalId\n  currency\n  eTransferEmail\n  eTransferName\n  externalCanonicalId\n  identityId\n  institutionName\n  occurredAt\n  p2pHandle\n  p2pMessage\n  spendMerchant\n  securityId\n  billPayCompanyName\n  billPayPayeeNickname\n  redactedExternalAccountNumber\n  opposingAccountId\n  status\n  subType\n  type\n  strikePrice\n  contractType\n  expiryDate\n  chequeNumber\n  provisionalCreditAmount\n  primaryBlocker\n  interestRate\n  frequency\n  counterAssetSymbol\n  rewardProgram\n  counterPartyCurrency\n  counterPartyCurrencyAmount\n  counterPartyName\n  fxRate\n  fees\n  reference\n  __typename\n}"
})
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0',
  'Accept': '*/*',
  'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Referer': 'https://my.wealthsimple.com/app/activity',
  'content-type': 'application/json',
  'authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJpZGVudGl0eS1fdlBMOUVncVJIN3dKWDVxQk9idlMxWDhlQSIsImV4cCI6MTczMjI2MDY4NCwiaWF0IjoxNzMyMjU4ODg0LCJqdGkiOiJxa0NKTDVsSUJsVVc3YW1hb1BpNnNlU0NURjRBYVk5SUQydHJVa01mX0xvIiwiY2xpZW50X2lkIjoiNGRhNTNhYzJiMDMyMjViZWQxNTUwZWJhOGU0NjExZTA4NmM3YjkwNWEzODU1ZTZlZDEyZWEwOGMyNDY3NThmYSIsInNjb3BlIjoiaW52ZXN0LnJlYWQgaW52ZXN0LndyaXRlIHRyYWRlLnJlYWQgdHJhZGUud3JpdGUgdGF4LnJlYWQgdGF4LndyaXRlIn0.K_N3lwIiJ77XxF_2-23KYkNwhynXjULXeJ_FnjZBxwSzhAsBIwjzJ32yMUBzrNBEkZXd3E68XNqsUeQSDf2qH-zubu8xiL0h2b1ik4BPnELxkCFz8hfRV8dUdcRIOEGkW8EjN32_8MglrCVQIYtgxS6X_xjkWH0YUAv68fVW0wUHjoTgQUrup_F9fi2UPkOaUgEblD4LEp2Q4c49CmDKy6bvl622JgILycAdtI3wEcnhYGiqXzMSr-2BoYHaw2e3eIlrXLm3d5HWMtRhjdhnFjtdqLM8DFF0m-TmMo4kzEWgwOa-00BBBmFpTc6AsVPTbwJM9mvC4zQFz4ZEEpnXKw',
  'x-ws-api-version': '12',
  'x-ws-locale': 'en-CA',
  'x-ws-profile': 'trade',
  'x-platform-os': 'web',
  'x-ws-device-id': 'c653a0845c50aa37c4439a4d17067ecb',
  'Origin': 'https://my.wealthsimple.com',
  'Connection': 'keep-alive',
  'Cookie': 'wssdi=c653a0845c50aa37c4439a4d17067ecb; _cfuvid=5K9Q0CAyQ9nzYbMe0nFnCYmdnQm6ASK.HlD5RnJKWtg-1732256253579-0.0.1.1-604800000; ws_global_visitor_id=c16773f5-4b54-4872-90e2-76134f44d63e; ws_referrer_url=none; ws_global_visitor_id=user_c905510e9e39ad413e46e2594e2a2b32; ws_jurisdiction=CA; _dd_s=rum=0&expire=1732259834098; _oauth2_access_v2=%7B%22access_token%22%3A%22eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJpZGVudGl0eS1fdlBMOUVncVJIN3dKWDVxQk9idlMxWDhlQSIsImV4cCI6MTczMjI2MDY4NCwiaWF0IjoxNzMyMjU4ODg0LCJqdGkiOiJxa0NKTDVsSUJsVVc3YW1hb1BpNnNlU0NURjRBYVk5SUQydHJVa01mX0xvIiwiY2xpZW50X2lkIjoiNGRhNTNhYzJiMDMyMjViZWQxNTUwZWJhOGU0NjExZTA4NmM3YjkwNWEzODU1ZTZlZDEyZWEwOGMyNDY3NThmYSIsInNjb3BlIjoiaW52ZXN0LnJlYWQgaW52ZXN0LndyaXRlIHRyYWRlLnJlYWQgdHJhZGUud3JpdGUgdGF4LnJlYWQgdGF4LndyaXRlIn0.K_N3lwIiJ77XxF_2-23KYkNwhynXjULXeJ_FnjZBxwSzhAsBIwjzJ32yMUBzrNBEkZXd3E68XNqsUeQSDf2qH-zubu8xiL0h2b1ik4BPnELxkCFz8hfRV8dUdcRIOEGkW8EjN32_8MglrCVQIYtgxS6X_xjkWH0YUAv68fVW0wUHjoTgQUrup_F9fi2UPkOaUgEblD4LEp2Q4c49CmDKy6bvl622JgILycAdtI3wEcnhYGiqXzMSr-2BoYHaw2e3eIlrXLm3d5HWMtRhjdhnFjtdqLM8DFF0m-TmMo4kzEWgwOa-00BBBmFpTc6AsVPTbwJM9mvC4zQFz4ZEEpnXKw%22%2C%22token_type%22%3A%22Bearer%22%2C%22expires_in%22%3A1800%2C%22refresh_token%22%3A%22lug18q5IsigdI1DrwahVI6Qyc98KKv-2b21taRv7AFQ%22%2C%22scope%22%3A%22invest.read%20invest.write%20trade.read%20trade.write%20tax.read%20tax.write%22%2C%22created_at%22%3A1732258884%2C%22okta_group_claims%22%3A%5B%5D%2C%22identity_canonical_id%22%3A%22identity-_vPL9EgqRH7wJX5qBObvS1X8eA%22%2C%22clock_skew%22%3A%7B%22skewed%22%3Afalse%7D%2C%22expires_at%22%3A%222024-11-22T07%3A31%3A24.000Z%22%2C%22email%22%3A%22wealthsimple%40astad.me%22%2C%22profiles%22%3A%7B%22tax%22%3A%7B%22default%22%3A%22user-0xgaydnxpyn%22%7D%2C%22trade%22%3A%7B%22default%22%3A%22user-vwnehczdi5r%22%7D%2C%22invest%22%3A%7B%22default%22%3A%22user-vzosidab6xm%22%7D%7D%2C%22client_canonical_ids%22%3A%7B%22tax%22%3A%7B%22default%22%3A%22person-aw1eualykrjngq%22%7D%2C%22trade%22%3A%7B%22default%22%3A%22person-ove4rzz14j_lfa%22%7D%2C%22invest%22%3A%7B%22default%22%3A%22person-wgxklpzj4prutg%22%7D%7D%2C%22suspended_profiles%22%3A%7B%7D%7D; _session_id=7a4bab0d458da046122a7c3a95646eb5; ab.storage.userId.80ec85f3-36f6-4cc8-8401-81fb1619363d=g%3Aidentity-_vPL9EgqRH7wJX5qBObvS1X8eA%7Ce%3Aundefined%7Cc%3A1732258897337%7Cl%3A1732258897337; ab.storage.sessionId.80ec85f3-36f6-4cc8-8401-81fb1619363d=g%3A31dd8dee-c1f3-5301-9b26-d5825be1d5cf%7Ce%3A1732259198686%7Cc%3A1732258897337%7Cl%3A1732258898686; ab.storage.deviceId.80ec85f3-36f6-4cc8-8401-81fb1619363d=g%3Af41f3698-bdab-3a9a-ff2d-e7b2ef2078aa%7Ce%3Aundefined%7Cc%3A1732258897337%7Cl%3A1732258897337',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Priority': 'u=4',
  'TE': 'trailers'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
