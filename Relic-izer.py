

Salvage = ["Carbonite circuit board", "Bronzium wiring", "Chromium transistor", "Aurodium heatsink",
           "Electrium conductor", "Zinbiddle card", "Impulse detector", "Aeromagnifier", "Gyrda keypad", "Droid brain"]
Signal_Data = ["Fragmented", "Incomplete", "Flawed"]

salvage_reqs = [
    [40, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Relic 0
    [30, 40, 0, 0, 0, 0, 0, 0, 0, 0],  # Relic 1
    [30, 40, 0, 0, 0, 0, 0, 0, 0, 0],  # Relic 2
    [30, 40, 40, 0, 0, 0, 0, 0, 0, 0],  # Relic 3
    [30, 40, 30, 20, 0, 0, 0, 0, 0, 0],  # Relic 4
    [20, 30, 30, 20, 20, 0, 0, 0, 0, 0],  # Relic 5
    [20, 30, 20, 20, 20, 10, 0, 0, 0, 0],  # Relic 6
    [0, 0, 20, 20, 20, 20, 20, 20, 0, 0],  # Relic 7
    [0, 0, 20, 20, 20, 20, 20, 20, 20, 20],  # Relic 8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Relic 9
    ]


signalData_reqs = [
        [0, 0, 0],  # Relic 0
        [15, 0, 0],  # Relic 1
        [20, 15, 0],  # Relic 2
        [20, 25, 0],  # Relic 3
        [20, 25, 15],  # Relic 4
        [20, 25, 25],  # Relic 5
        [20, 25, 35],  # Relic 6
        [20, 25, 45],  # Relic 7
        [30, 30, 55],  # Relic 8
        [0, 0, 0],  # Relic 9
        ]


def calculate_mats(relic):

        if relic < 0 or relic > 8:
                print("Only number can be used, you twat. Try again")
                return None, None
        salvage_needed = salvage_reqs[relic]
        signalData_needed = signalData_reqs[relic]

        return salvage_needed, signalData_needed


def calculate_mats_sum(current_relic, target_relic):

        total_salvage_dif = [0] * len(Salvage)
        total_signalData_dif = [0] * len(Signal_Data)

        for relic_level in range(current_relic, target_relic):
            salvage_needed, signalData_needed = calculate_mats(relic_level)

            if salvage_needed is not None and signalData_needed is not None:
                total_salvage_dif = [total + req for total, req in zip(total_salvage_dif, salvage_needed)]
                total_signalData_dif = [total + req for total, req in zip(total_signalData_dif, signalData_needed)]

        return total_salvage_dif, total_signalData_dif


def user_input():

        try:
            current_relic = input("What's your current Relic level?: ")  # Prompt for current relic level
            target_relic = input("What's your target Relic level? [1 to 9]: ")  # Prompt for target relic level

            # Check if both inputs are numeric
            if not current_relic.isdigit() or not target_relic.isdigit():
                print("Invalid input. Please enter numbers between 1-9.")
                return None, None

            # Convert inputs to integers
            current_relic = int(current_relic)
            target_relic = int(target_relic)

            # Check if the input is within valid relic levels (0-8 for current relic, 1-9 for target relic)
            if current_relic < 0 or current_relic > 8:
                print("Invalid current Relic level. Please enter a value between 0 and 8.")
                user_input()

            if target_relic < 1 or target_relic > 9:
                print("Invalid target Relic level. Please enter a value between 1 and 9.")
                user_input()

            if current_relic > target_relic:
                print("You can't go backwards in Relic levels.")
                user_input()

            if current_relic == target_relic:
                print("this is a Relic UPGRADING calculation tool. Use it as such, you ninny.")
                user_input()

            return current_relic, target_relic
        except ValueError:
            # This block is for handling any unexpected errors in conversion or other input issues
            print("Invalid input. Please enter valid Relic levels.")
            return None, None


current_relic, target_relic = user_input()

if current_relic is not None and target_relic is not None:

            total_salvage_dif, total_signalData_dif = calculate_mats_sum(current_relic,
                                                                         9 if target_relic == 9 else target_relic)

            if total_salvage_dif and total_signalData_dif:
                print(f"\nOK, to get yourself from Relic {current_relic} to Relic {target_relic} you'll need:")
                print('========\nSalvage\n========')
                for salvage, diff in zip(Salvage, total_salvage_dif):
                        print(f"{salvage}s: {diff} pieces")

                print('============\nSignal Data\n============')
                for signalData, diff in zip(Signal_Data, total_signalData_dif):
                        print(f"{signalData}: {diff} mats")
