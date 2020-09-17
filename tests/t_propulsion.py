import unittest
import os
import pandas as pd
import math

from ADRpy import propulsion as decks

# A list of possible engine types. This list is included here to avoid the need
# for an init function in the class.
ENGINE_TYPE = ["jet", "piston", "turboprop", "electric"]
# A list of dictionaries for all types.This list is included here to avoid the
# need for an init function in the class.
ENGINE_DICTS = [decks.local_data(specific_type, printdata=False) for specific_type in ENGINE_TYPE]


class TestPropulsionDeck(unittest.TestCase):
    """
    Tests that all engines are listed and the engines that are listed have data
    associated with them. It uses that data that was used as input data to
    produce the functions. The tests ensure that the output data is within 1%
    of the original input data.
    """

    def test_names(self):
        """
        This test ensures that each engine described in the local data csv
        has a csv associated with it and that each engine with data provided
        has a corresponding entry in the local data csv.
        """
        print("Tests Stored data and Local_data")
        # defaults data to true
        data = True
        # Goes through each engine type
        for index, engine_type in enumerate(ENGINE_TYPE):
            # Finds engine dictionary from list
            engine_dict = ENGINE_DICTS[index]
            # Creates a list of engines stored for verification.
            engine_list = list(engine_dict.keys())
            # Creates an empty list for the data found by the local_data
            # function.
            known_data = []
            # for each engine in each category.
            for engine in engine_list:
                csvs = engine_dict[engine]['available_data']
                # Creates a list of all data.
                known_data += csvs
                if len(csvs) == 0:
                    # Sets data to false if no CSVs are found for a particular
                    # function
                    data = False
                    # Breaks out of for look
                    break
            # -1 is because of the data available csv.
            file_count = len(os.listdir(
                os.path.join(os.path.dirname(decks.__file__), "data", "engine data", engine_type + " CSVs"))) - 1
            # Checks to see if the files counted in the CSV folder matches the
            # total from the data list.
            if file_count != len(known_data):
                print(engine_type, file_count, len(known_data))
                data = False
            # Breaks if data is set to False.
            if data is False:
                break
        self.assertTrue(data)

    def test_jet_values(self):
        """
        Tests jet engines by using the data gathered and taking a selection of
        points and then comparing them to the values generated by the function.
        """
        print("Tests Jet Thrust and TSFC Data.")
        # Creates list of engines.
        engine_list = list(ENGINE_DICTS[0].keys())
        engine_type = "Jet"  # Based on the jet engine type.
        input1_list = ["Mach Number", "Mach Number"]  # Inputs for engine deck.
        input2_list = ["Altitude (m)", "Thrust (N)"]  # Inputs for engine deck.
        # Returned values for each of the inputs.
        output_list = ["Thrust (N)", "TSFC (g/(kNs))"]
        fun_list = ["thrust", "tsfc"]
        # For each engine in the list of engines do the following.
        self.assertTrue(_deck_csvtester(engine_list, engine_type, input1_list,
                                        input2_list, output_list, fun_list,
                                        fun_list, decks.JetDeck))

    def test_turboprop_values(self):
        """
        Tests turboprop engines by using the data gathered and taking a
        selection of points and then comparing them to the values generated
        by the function.
        """
        print("Tests Turboprop Thrust, BSFC and Power Data.")
        # Creates list of engines.
        engine_list = list(ENGINE_DICTS[2].keys())
        engine_type = "turboprop"  # Based on the turboprop engine type
        # Inputs for engine deck.
        input1_list = ["Mach Number", "Mach Number", "Mach Number"]
        # Inputs for engine deck
        input2_list = ["Altitude (m)", "Altitude (m)", "Altitude (m)"]
        # Returned values for each of the inputs.
        output_list = ["Thrust (N)", "BSFC (g/(kWh))", "Power (W)"]
        fun_list = ["hotthrust", "tsfc", "shaftpower"]
        # For each engine in the list of engines do the following.
        self.assertTrue(_deck_csvtester(engine_list, engine_type, input1_list, input2_list, output_list, fun_list,
                                        fun_list, decks.TurbopropDeck))

    def test_piston_values(self):
        """
        Tests piston engines by using the data gathered and taking a
        selection of points and then comparing them to the values generated
        by the function.
        """
        print("Tests Piston power, best BSFC and most economical BSFC Data.")
        # Creates list of engines.
        engine_list = list(ENGINE_DICTS[1].keys())
        engine_type = "piston"  # Based on the piston engine type.
        # Inputs for engine deck.
        input1_list = ["Speed (RPM)", "Speed (RPM)", "Speed (RPM)"]
        # Inputs for engine deck.
        input2_list = ["Altitude (m)", "Power (W)", "Power (W)"]
        # Returned values for each of the two inputs.
        output_list = ["Power (W)", "BSFC (g/(kWh))", "BSFC (g/(kWh))"]
        fun_list = ["shaftpower", "bsfc", "bsfc"]
        file_name_list = ["power", "bsfc best power", "bsfc"]
        attr = [None, None, "economy"]
        # For each engine in the list of engines do the following.
        self.assertTrue(_deck_csvtester(engine_list, engine_type, input1_list, input2_list, output_list, fun_list,
                                        file_name_list, decks.PistonDeck, attr=attr))

    def test_electric_values(self):
        """
        Tests electric engines by using the data gathered and taking a
        selection of points and then comparing them to the values generated
        by the function.
        """
        print("Tests Electric engine Efficiency.")
        # Creates list of engines.
        engine_list = list(ENGINE_DICTS[3].keys())
        engine_type = "electric"  # Based on the electric engine type.
        input1_list = ["Speed (RPM)"]  # Inputs for engine deck.
        input2_list = ["Torque (Nm)"]  # Inputs for engine deck.
        # Returned values for each of the inputs.
        output_list = ["Efficiency"]
        fun_list = ["efficiency"]
        # For each engine in the list of engines do the following.
        self.assertTrue(_deck_csvtester(engine_list, engine_type, input1_list, input2_list, output_list, fun_list,
                                        fun_list, decks.ElectricDeck))

    def test_jet_poly(self):
        """
        Tests jet engines sea level polynomial curves by using the data.
        gathered and taking a selection of points and then comparing them to
        the values generated by the function.
        """
        print("Tests Jet Sea level and Take off Thrust polynomial functions")
        # Creates list of engines.
        engine_list = list(ENGINE_DICTS[0].keys())
        engine_type = "Jet"  # Based on the jet engine type.
        input1_list = ["Mach Number"] * 2  # Inputs for engine deck.
        input2_list = ["Altitude (m)"] * 2  # Inputs for engine deck.
        # Returned values for each of the inputs.
        output_list = ["Thrust (N)"] * 2
        fun_list = ["sl_thrust", "sl_take_off_thrust"]
        file_name_list = ["thrust", "sl to thrust"]
        # For each engine in the list of engines do the following.
        self.assertTrue(_deck_csvtester(engine_list, engine_type, input1_list, input2_list, output_list, fun_list,
                                        file_name_list, decks.JetDeck, alt=0, x_only=True))

    def test_propeller_etasolver(self):
        """
        Tests the implemented method for estimating propeller efficiency from geometrical parameters.
        """
        print("Tests Propeller efficiency solver")

        propellerconcept = {'diameter_m': 2.67, 'bladecount': 4, 'bladeactivityfact': 100, 'idesign_cl': 0.5}

        testprop = decks.PropellerDeck(propeller=propellerconcept)
        eta = testprop.efficiency(mach=0.5026, altitude_m=8382, shaftpower_w=522000, prop_rpm=2000)
        self.assertEqual(round(float(eta), 5), round(0.8976928369352944, 5))


def _deck_csvtester(engine_list, engine_type, input1_list, input2_list, output_list, fun_list, file_name_list,
                    class_required, alt=None, attr=None, x_only=False):
    """
    **Parameters:**
    engine_list:
        List of engines.

    deck_type:
        String containing the type of engine under test.

    input1_list
        List of "x" value columns, each column corresponds to a function
        in fun_list.

    input2_list
        List of "y" value columns, each column corresponds to a function
        in fun_list.

    output_list
        List of "f(x,y)" values. This column contains data that is a
        function of both x and y.

    fun_list.
        list of functions. This contains the functions to apply to each
        of the items in the lists: input1_list, input2_list to produce the
        output which is then compared to: output_list.

    file_name_list
        list of files to search to find the x, y and z data. Again each
        column has a corresponding function in fun_list.

    class_required
        class to use.

    alt=None
        If alt is not None, then this means that the function will only
        take data from a given altitude (m) and uses all data at that
        altitude (m).

    attr=None.
        Attribute applied to function being investigated.

    x_only
        A boolean statement that indicates whether a function has only x or
        x and y input. If False then there is both x and y inputs accepted.
        If True then only the data from the list input1_list will be used.

    **Outputs:**
        True or False. If True then the functions applied to the x and y data
        match the actual data (output_list) within 1% then True will be
        returned. Otherwise False will be returned.
    """
    # Runs tests for each output. e.g. thrust, TSFC, Power BSFC etc.
    for name_index, output_name in enumerate(output_list):
        # Checks to see if attr (attribute)
        if attr is None:
            attrb = None  # Sets attribute to None if no data is provided
        else:
            # Else the attribute is found from a list.
            attrb = attr[name_index]
        # For each engine in the list of engines do the following
        for engine in engine_list:
            propulsor = class_required(engine)
            # Find and load the thrust data using Pandas.
            test_data = _std_csv_name_read(engine_type, engine, file_name_list[name_index])
            # If there is data available, then use the deck search function to
            # find the actual output at the values and the predicted output.
            if test_data is not None:
                thrust_n, predicted_thrust_n = _deck_search(test_data, getattr(propulsor, fun_list[name_index]),
                                                            input1_list[name_index], input2_list[name_index],
                                                            output_name, alt, attrb, x_only)
                for index, thrust_value_n in enumerate(thrust_n):
                    # Checks to see if the predicted data matches with the
                    # actual data.
                    percent = 100 * float(predicted_thrust_n[index]) / float(thrust_value_n)
                    if percent > 101 or percent < 99:
                        # If the results do not match then False is returned.
                        return False
    # If all data matches, then return True
    return True


def _std_csv_name_read(engine_type, engine, file_name):
    """
    **Parameters:**
        deck_type
            A string which contains one of the four listed families of
            aero-engine, which are: jet, piston, turboprop, electric.

        engine
            A string containing the specific type of engine being searched for

        file_name
            A string containing data that is part of the csv file name.

    **Outputs:**
        A pandas dataframe containing the information from the requested csv or
        nothing if it could not be found.
    """
    # Tries to see if file exists
    try:
        data_frame = (pd.read_csv(os.path.join(os.path.dirname(decks.__file__), "data", "engine data",
                                               engine_type + " CSVs", engine + " " + file_name + " data.csv")))
    except FileNotFoundError:
        # If not then noting is returned
        return
    # Returns data if it is available.
    return data_frame


def _deck_search(data, function, x, y, z, alt, attr=None, x_only=False):
    """
    **Parameters:**

    data
        pandas dataframe containing the data

    x
        string which matches a column heading in data.

    y
        string which matches a column heading in data.

    z
        string which matches a column heading in data.

    alt
        a number which defines an altitude (m) to investigate. If set as
        None then a sample of altitudes will be taken at every fifth value
        in the csv. If set to an altitude to investigate then it will take
        all values at the given altitude.

    attr
        Attribute applied to function being investigated. If set to None
        then no attribute will be applied to function being used.

    x_only
        A boolean statement that indicates whether a function has only x or
        x and y input. If False then there is both x and y inputs accepted.
        If True then only the data from the list input1_list will be used.

    **Outputs:**

    output
        list, containing the actual output data.

    output_predict
        list, containing the predicted output data.
    """
    if alt is None:
        length = len(data)  # Finds length of the data.
        step = math.floor(length / 5)  # Finds the step size
    else:
        # If Alt has a value, filter the dataframe by that value.
        data = data[data["Altitude (m)"] == alt]
        step = 1
    output = []
    output_predict = []
    for index in range(0, len(data) - 1, step):  # Creates an index
        input_x = data.loc[index][x]  # Finds input x data.
        input_y = data.loc[index][y]  # Finds input y data.
        output_z = data.loc[index][z]  # Finds output z data.
        # Checks to see if additional attribute has been added
        if attr is None:
            # Checks to see if function accepts only an x value
            if x_only is False:
                output_predict_z = function(input_x, input_y)
            else:
                output_predict_z = function(input_x)
        else:
            output_predict_z = function(input_x, input_y, attr)
        # Checks to see if output is nan type
        if pd.isnull(output_z) or pd.isnull(output_predict_z):
            pass
        else:
            output.append(output_z)  # Finds output data.
            # Creates a thrust prediction.
            output_predict.append(output_predict_z)
    return output, output_predict


if __name__ == '__main__':
    unittest.main()
