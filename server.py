# server
import csv
import logging
import asyncio
import time
from math import sin, cos, pi
from opcua import Server, ua
from collections import defaultdict

logging.getLogger("opcua.server.address_space").setLevel(logging.ERROR)
logging.getLogger("asyncua").setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO)

class OPCUAServerWrapper:
    def __init__(self, endpoint="opc.tcp://0.0.0.0:4840/freeopcua/server/", namespace_uri="localhost/opcua"):
        self.server = Server()
        self.server.set_endpoint(endpoint)
        self.idx = self.server.register_namespace(namespace_uri)
        self.objects_node = self.server.get_objects_node()
        self.device_nodes = {}
        self.device_vars = defaultdict(dict)
        self.simulated = []

    async def start(self):
        self.server.start()

    async def stop(self):
        self.server.stop()

    def parse_value(self, value_str):
        if value_str.lower() in ("true", "false"):
            return value_str.lower() == "true"
        try:
            if '.' in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            return value_str

    def parse_engineering_range(self, range_str):
        try:
            parts = range_str.split("..")
            if len(parts) == 2:
                return float(parts[0]), float(parts[1])
        except Exception:
            pass
        return None

    def get_ua_type(self, type_str):
        mapping = {
            "Double": ua.VariantType.Double,
            "Float": ua.VariantType.Float,
            "Int32": ua.VariantType.Int32,
            "Int16": ua.VariantType.Int16,
            "UInt32": ua.VariantType.UInt32,
            "UInt16": ua.VariantType.UInt16,
            "Boolean": ua.VariantType.Boolean,
            "String": ua.VariantType.String
        }
        return mapping.get(type_str, ua.VariantType.String)

    async def load_from_csv(self, filepath):
        with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    device = row["Device"].strip()
                    var_name = row["Name"].strip()
                    value = self.parse_value(row["Value"].strip())
                    nodeid_str = row["NodeId"].strip()
                    datatype = self.get_ua_type(row["DataType"].strip())
                    writable = row["Writable"].strip().lower() == "true"
                    unit = row["Unit"].strip()
                    desc = row["Description"].strip()
                    eng_range = self.parse_engineering_range(row["EngineeringRange"].strip())
                    sim_type = row.get("Simulated", "").strip().lower()

                    dev_node = self.device_nodes.setdefault(device, self.objects_node.add_object(self.idx, device))

                    var = dev_node.add_variable(nodeid_str or f"{self.idx}:{var_name}", var_name, ua.Variant(value, datatype))
                    if writable:
                        var.set_writable()
                    if desc:
                        var.set_attribute(ua.AttributeIds.Description, ua.DataValue(ua.LocalizedText(desc)))
                    if unit:
                        var.add_property(self.idx, "Unit", unit)
                    if eng_range:
                        r = ua.Range()
                        r.Low, r.High = eng_range
                        var.add_property(self.idx, "EngineeringRange", r)

                    self.device_vars[device][var_name] = var
                    if sim_type in ("sin", "cos"):
                        self.simulated.append((var, sim_type, eng_range))
                except Exception as e:
                    logging.error(f"Ошибка при загрузке строки: {e}")

    async def simulate_loop(self):
        while True:
            t = time.time()
            for var, sim_type, eng_range in self.simulated:
                if eng_range:
                    low, high = eng_range
                    amplitude = (high - low) / 2
                    offset = low + amplitude
                    value = offset + amplitude * (sin(2 * pi * 0.01 * t) if sim_type == "sin" else cos(2 * pi * 0.01 * t))
                    var.set_value(round(value, 2))
            await asyncio.sleep(1)

async def main():
    import os
    path = input("Введите путь к CSV-файлу: ").strip()
    while not os.path.isfile(path):
        path = input("Файл не найден. Повторите ввод: ").strip()

    server = OPCUAServerWrapper()
    await server.load_from_csv(path)

    await server.start()
    logging.info("🚀 Сервер запущен. Нажмите Ctrl+C для остановки.")
    try:
        await server.simulate_loop()
    except KeyboardInterrupt:
        logging.info("🛑 Остановка сервера...")
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())
