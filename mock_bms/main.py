from data_gen import generate_and_store_data, retrieve_stored_battery_data, run_battery_data_generator

if __name__ == '__main__':
    print(run_battery_data_generator())

    generate_and_store_data()

    print(retrieve_stored_battery_data())
