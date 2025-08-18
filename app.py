from flask import Flask, render_template, request
import requests

app = Flask(__name__)

CORPORATE_LOGIN_URL = "http://54.89.241.89:5000/login"

OTHER_APIS = [
    {
        "name": "MaToMA Inquiry",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/MaToMA/Inquiry",
        "method": "POST",
        "headers": {
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "accept": "application/json",
            "content-type": "application/json",
            "X-Channel": "subgateway"
        },
        "body": {
            "Amount": "20",
            "MSISDN": "923319154345",
            "ReceiverMSISDN": "923355923388",
            "cnic": "3700448243372"
        }
    },
    {
        "name": "MaToMA Transfer",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/MaToMA/Transfer",
        "method": "POST",
        "headers": {
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "accept": "application/json",
            "content-type": "application/json",
            "X-Channel": "subgateway"
        },
        "body": {
            "Amount": "10",
            "MSISDN": "923319154345",
            "ReceiverMSISDN": "923355923388"
        }
    },
    {
        "name": "Subscriber IBFT Inquiry",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/SubscriberIBFT/Inquiry",
        "method": "POST",
        "headers": {
            "X-Channel": "subgateway",
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "accept": "application/json",
            "content-type": "application/json"
        },
        "body": {
            "Amount": "47",
            "BankShortName": "MOD",
            "BankTitle": "MOD",
            "AccountNumber": "00020000011005325",
            "MSISDN": "923319154345",
            "ReceiverMSISDN": "923332810960",
            "ReceiverIBAN": "",
            "TransactionPurpose": "0350"
        }
    },
    {
        "name": "Subscriber IBFT Transfer",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/SubscriberIBFT/Transfer",
        "method": "POST",
        "headers": {
            "X-Channel": "subgateway",
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "accept": "application/json",
            "content-type": "application/json"
        },
        "body": {
            "Amount": "47",
            "BankShortName": "MOD",
            "BankTitle": "MOD",
            "Branch": "00",
            "AccountNumber": "00020000011005325",
            "MSISDN": "923319154345",
            "ReceiverMSISDN": "923332810960",
            "ReceiverIBAN": "",
            "SenderName": "ZEESHAN AHMED",
            "TransactionPurpose": "0350",
            "Username": "ZEESHAN AHMED"
        }
    },
    {
        "name": "MAtoCNIC Inquiry",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/MAtoCNIC/Inquiry",
        "method": "POST",
        "headers": {
            "X-Channel": "subgateway",
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "accept": "application/json",
            "content-type": "application/json"
        },
        "body": {
            "Amount": "15",
            "MSISDN": "923319154345",
            "ReceiverMSISDN": "923355923388",
            "ReceiverCNIC": "3520207345019"
        }
    },
    {
        "name": "MAtoCNIC Transfer",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/MAtoCNIC/Transfer",
        "method": "POST",
        "headers": {
            "X-Channel": "subgateway",
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "accept": "application/json",
            "content-type": "application/json"
        },
        "body": {
            "Amount": "15",
            "MSISDN": "923319154345",
            "ReceiverMSISDN": "923482665224",
            "ReceiverCNIC": "3520207345019"
        }
    },
    {
        "name": "Subscriber Utility Bill Inquiry",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/SubscriberUtilityBill/Inquiry",
        "method": "POST",
        "headers": {
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "accept": "application/json",
            "content-type": "application/json",
            "X-Channel": "subgateway"
        },
        "body": {
            "ConsumerNumber": "05131220253300",
            "MSISDN": "923319154345",
            "Company": "PESCO"
        }
    },
    {
        "name": "Subscriber Utility Bill Payment",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/SubscriberUtilityBill/Payment",
        "method": "POST",
        "headers": {
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "accept": "application/json",
            "content-type": "application/json",
            "X-Channel": "subgateway"
        },
        "body": {
            "Amount": "100.00",
            "ConsumerNumber": "01261110004080",
            "MSISDN": "923319154345",
            "Company": "PESCO"
        }
    },
    {
        "name": "Account Balance",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/account-balance/account-bal",
        "method": "POST",
        "headers": {
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "X-Channel": "subgateway",
            "Content-Type": "application/json"
        },
        "body": {
            "msisdn": "923319154345"
        }
    },
    {
        "name": "Transaction Status Inquiry",
        "url": "https://rgw.8798-f464fa20.eu-de.ri1.apiconnect.appdomain.cloud/tmfb/dev-catalog/transaction-status-inquiry/TransactionStatusInquiry",
        "method": "POST",
        "headers": {
            "X-IBM-Client-Id": "924726a273f72a75733787680810c4e4",
            "X-IBM-Client-Secret": "7154c95b3351d88cb31302f297eb5a9c",
            "accept": "application/json",
            "content-type": "application/json",
            "X-Channel": "subgateway"
        },
        "body": {
            "transactionID": "5088215"
        }
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        msisdn = request.form.get("msisdn")
        pin = request.form.get("pin")

        if not msisdn or not pin:
            return render_template("index.html", error="Please enter both MSISDN and PIN.")

        # Corporate Login
        login_headers = {
            "Content-Type": "application/json"
        }
        login_payload = {
            "msisdn": msisdn,
            "pin": pin
        }

        try:
            login_resp = requests.post(CORPORATE_LOGIN_URL, headers=login_headers, json=login_payload)
            login_resp.raise_for_status()
            login_data = login_resp.json()
        except Exception as e:
            return render_template("index.html", error=f"Login API error: {str(e)}")

        x_hash = login_data.get("X-Hash") or login_data.get("x-hash") or login_data.get("X-Hash-Value")
        if not x_hash:
            return render_template("index.html", error=f"X-Hash not found in login response: {login_data}")

        #Update all API bodies to use the login MSISDN
        for api in OTHER_APIS:
            body = api.get("body", {})
            for key in body:
                if key.lower() == "msisdn":  # only sender, not receiver
                    body[key] = msisdn

                #Store TransactionReference from MaToMA Transfer
        transaction_reference_from_matoma = None

        # Call other APIs with X-Hash
        for api in OTHER_APIS:
            headers = api["headers"].copy()
            headers["X-Hash-Value"] = x_hash

            try:
                # Make a fresh copy of body
                body = api.get("body", {}).copy()

                # Only replace sender MSISDN
                for key in body:
                    if key.lower() == "msisdn":
                        body[key] = msisdn

                #Inject the TransactionReference into Transaction Status Inquiry
                if api["name"] == "Transaction Status Inquiry" and transaction_reference_from_matoma:
                    body["transactionID"] = transaction_reference_from_matoma

                # Send request
                if api["method"].upper() == "POST":
                    resp = requests.post(api["url"], headers=headers, json=body)
                else:
                    resp = requests.get(api["url"], headers=headers, params=body)

                try:
                    resp_data = resp.json()
                except:
                    resp_data = resp.text

                #Capture TransactionReference from MaToMA Transfer response
                if api["name"] == "MaToMA Transfer" and isinstance(resp_data, dict):
                    transaction_reference_from_matoma = (
                        resp_data.get("TransactionReference") or 
                        resp_data.get("transactionReference")
                    )

                results.append({
                    "name": api["name"],
                    "status_code": resp.status_code,
                    "response": resp_data
                })

            except Exception as e:
                results.append({
                    "name": api["name"],
                    "status_code": "Error",
                    "response": str(e)
                })

        return render_template("index.html", results=results, msisdn=msisdn)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
