def test_get_DRDmeasurement_model(client):
    res = client.get("/drdmeasurement/id/000000a5-07eb-4385-9fac-8a79b403f229")
    assert res.status_code == 200
    assert res.json() == {'id': '000000a5-07eb-4385-9fac-8a79b403f229', 'distance': '33666,76989346', 'tag': 'Profilometer', 'lat': 55.707497, 'lon': 12.514463, 'message': '{"Laser1":85.349443688,"Laser2":74.010046942,"Laser3":63.946175197,"Laser4":53.639125118,"Laser5":47.439839473,"Laser6":41.322145996,"Laser7":35.179144025,"Laser8":29.676212166,"Laser9":23.801565564,"Laser10":18.338481462,"Laser11":11.877015239,"Laser12":3.309950893,"Laser13":-8.272389186,"Laser14":-20.821291766,"Laser15":-28.900410107,"Laser16":-34.088728584,"Laser17":-40.174078311,"Laser18":-46.175053038,"Laser19":-52.616887643,"Laser20":-58.536611868,"Laser21":-64.52532097,"Laser22":-70.769967573,"Laser23":-80.567859882,"Laser24":-90.852272209,"Laser25":-102.123347381}', 'is_computed': True, 'fk_trip': '8b5b28b0-9034-4ee4-9cd2-6cc636a2b328', 'fk_measurement_type': '7017e64d-a58f-4362-9dc6-a7b07f3d6d99', 'created_date': '2020-07-14T22:00:00+00:00', 'updated_date': '2020-07-14T22:00:00+00:00'}

def test_get_DRDmeasurement_model(client):
    res = client.get("/drdmeasurement/id/7017e64d-a58f-4362-9dc6-a7b07f3d6d99")
    assert res.status_code == 404
    assert res.json() == {'detail': 'drdmeasurement not found'}

