from locust import HttpUser, task, between


class PerformanceTests(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_predict_batch(self):
        # Create sample data
        data = {
            "data": [
                {
                    "x0": 0.042317,
                    "x1": -3.344721,
                    "x2": 4.6351242122,
                    "x3": -0.5983959993,
                    "x4": -0.6477715046,
                    "x5": "monday",
                    "x6": 0.184902,
                    "x7": 46.690015,
                    "x8": 3.034132,
                    "x9": 0.364704,
                    "x10": 14.260733,
                    "x11": -1.559332,
                    "x12": "$5,547.78",
                    "x13": 0.520324,
                    "x14": 31.212255,
                    "x15": 4.891671,
                    "x16": 0.357763,
                    "x17": 14.766366,
                    "x18": -17.467243,
                    "x19": 0.224628,
                    "x20": 0.096752,
                    "x21": 1.305564,
                    "x22": 0.353632,
                    "x23": 3.909028,
                    "x24": -91.273052,
                    "x25": 1.396952,
                    "x26": 4.401593,
                    "x27": 0.443086,
                    "x28": 14.048787,
                    "x29": -0.932243,
                    "x30": 5.255472,
                    "x31": "germany",
                    "x32": 0.54199153,
                    "x33": 2.98948039,
                    "x34": -1.78334189,
                    "x35": 0.80127315,
                    "x36": -2.60231221,
                    "x37": 3.39682926,
                    "x38": -1.22322646,
                    "x39": -2.20977636,
                    "x40": -68.69,
                    "x41": 522.25,
                    "x42": -428.69,
                    "x43": 381.37,
                    "x44": 0.0197503,
                    "x45": 0.75116479,
                    "x46": 0.8630479008,
                    "x47": -1.0383166613,
                    "x48": -0.2726187635,
                    "x49": -0.3430207259,
                    "x50": 0.3109008666,
                    "x51": -0.797841974,
                    "x52": -2.0390175153,
                    "x53": 0.87182889,
                    "x54": 0.14373012,
                    "x55": -1.15212514,
                    "x56": -2.1703139704,
                    "x57": -0.267842962,
                    "x58": 0.212110633,
                    "x59": 1.6926559407,
                    "x60": -0.9522767913,
                    "x61": -0.8625864974,
                    "x62": 0.0748487158,
                    "x63": "36.29%",
                    "x64": 3.47125327,
                    "x65": -3.16656509,
                    "x66": 0.65446814,
                    "x67": 14.60067029,
                    "x68": -20.57521013,
                    "x69": 0.71083785,
                    "x70": 0.16983767,
                    "x71": 0.55082127,
                    "x72": 0.62814576,
                    "x73": 3.38608078,
                    "x74": -112.45263714,
                    "x75": 1.48370808,
                    "x76": 1.77035368,
                    "x77": 0.75702363,
                    "x78": 14.75731742,
                    "x79": -0.62550355,
                    "x80": None,
                    "x81": "October",
                    "x82": "Female",
                    "x83": -0.7116680715,
                    "x84": -0.2653559892,
                    "x85": 0.5175495907,
                    "x86": -1.0881027092,
                    "x87": -1.8188638198,
                    "x88": -1.3584469527,
                    "x89": -0.654995195,
                    "x90": -0.4933042262,
                    "x91": 0.373853,
                    "x92": 0.94143481,
                    "x93": 3.54679834,
                    "x94": -99.8574882,
                    "x95": 0.403926,
                    "x96": 1.65378726,
                    "x97": 0.00771459,
                    "x98": -32.02164582,
                    "x99": -60.3127828
                }
            ]
        }

        # Send POST request to the FastAPI endpoint
        response = self.client.post("/predict", json=data)

        assert response.status_code == 200
        result = response.json()
        assert "class_probability" in result
        assert "input_variables" in result
        assert "predicted_class" in result
        print('Result', result)
