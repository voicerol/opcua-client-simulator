# simulate
import time
import logging
from opcua import Client, ua

SERVER_URL = "opc.tcp://localhost:4840/freeopcua/server/"

def is_numeric(variant_type):
    return variant_type in (
        ua.VariantType.Double,
        ua.VariantType.Float,
        ua.VariantType.Int32,
        ua.VariantType.Int16,
        ua.VariantType.UInt32,
        ua.VariantType.UInt16,
    )

def simulate():
    client = Client(SERVER_URL)
    try:
        client.connect()
        logging.info("🔌 Подключено к серверу")
        root = client.get_root_node()
        devices = root.get_child(["0:Objects"]).get_children()
        while True:
            for dev in devices:
                dev_name = dev.get_browse_name().Name
                for var in dev.get_variables():
                    try:
                        if not var.get_writable():
                            continue
                        try:
                            eng_range = var.get_child("2:EngineeringRange").get_value()
                            lo, hi = eng_range.Low, eng_range.High
                        except:
                            continue
                        variant_type = var.get_data_type_as_variant_type()
                        if not is_numeric(variant_type):
                            continue
                        # Оставим как резервную случайную симуляцию
                        new_val = lo + ((hi - lo) / 2)
                        var.set_value(ua.Variant(new_val, variant_type))
                        logging.info(f"🔄 [{dev_name}] {var.get_browse_name().Name} → {new_val}")
                    except Exception as e:
                        logging.error(f"Ошибка обновления {var.get_browse_name().Name}: {e}")
            time.sleep(5)
    except Exception as e:
        logging.error(f"❌ Ошибка подключения: {e}")
    finally:
        client.disconnect()
        logging.info("🔌 Отключено от сервера")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    simulate()
