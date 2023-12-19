from settings import NAMA_HP_SCALE

class BaseMethod():

    def __init__(self, data_dict, **setWeight):

        self.dataDict = data_dict

        # 1-6 (Kriteria)
        self.raw_weight = {
            'nama_hp': 1,
            'ram': 2,
            'processor': 3,
            'baterai': 4,
            'harga': 5,
            'ukuran_layar': 6
        }

        if setWeight:
            for item in setWeight.items():
                temp1 = setWeight[item[0]] # value int
                temp2 = {v: k for k, v in setWeight.items()}[item[1]] # key str

                setWeight[item[0]] = item[1]
                setWeight[temp2] = temp1

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        print(self.dataDict)
        return [{
            'id': smartphone['nama_hp'],
            'nama_hp': NAMA_HP_SCALE[smartphone['nama_hp']],
            'ram': smartphone['ram'],
            'processor': smartphone['processor'],
            'baterai':smartphone['baterai'],
            'harga': smartphone['harga'],
            'ukuran_layar': smartphone['ukuran_layar']
        } for smartphone in self.dataDict]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]

        nama_hp = [] # max
        ram = [] # max
        processor = [] # max
        baterai = [] # max
        harga = [] # min
        ukuran_layar = [] # max

        for data in self.data:
            nama_hp.append(data['nama_hp'])
            ram.append(data['ram'])
            processor.append(data['processor'])
            baterai.append(data['baterai'])
            harga.append(data['harga'])
            ukuran_layar.append(data['ukuran_layar'])

        max_nama_hp = max(nama_hp)
        max_ram = max(ram)
        max_processor = max(processor)
        max_baterai = max(baterai)
        min_harga = min(harga)
        max_ukuran_layar = max(ukuran_layar)

        return [{
            'id': data['id'],
            'nama_hp': data['nama_hp']/max_nama_hp, # benefit
            'ram': data['ram']/max_ram, # benefit
            'processor': data['processor']/max_processor, # benefit
            'baterai': data['baterai']/max_baterai, # benefit
            'harga': min_harga/data['harga'], # cost
            'ukuran_layar': data['ukuran_layar']/max_ukuran_layar # benefit
        } for data in self.data]
 

class WeightedProduct(BaseMethod):
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)

    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight[WP]
        result = {row['id']:
            round(
                row['nama_hp'] ** weight['nama_hp'] *
                row['ram'] ** weight['ram'] *
                row['processor'] ** weight['processor'] *
                row['baterai'] ** weight['baterai'] *
                row['harga'] ** (-weight['harga']) *
                row['ukuran_layar'] ** weight['ukuran_layar']
                , 3
            )

            for row in self.normalized_data}
        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))
