def check_consistency(source, series_wos, dict_real_wos):
    """Test unit for the Web of Science/Zoological Records data extraction

        Args:
            source (str): Name of the source
            series_wos (pandas.Series): Contains the value counts per year from the extracted data
            dict_real_wos (dict): Contains the actual observed results from WoS GUI
    """
    wos_total_results = sum(dict_real_wos.values())

    print('-'*74)                   # Begin with my cool divider
    print("Testing for... {}".format(source.upper()))
    print('-'*74)                   # Print a cool divider

    # Assertions about the total counts
    try:
        assert(wos_total_results == series_wos.sum())
        print("SUCCESS! Total count was equal between the processed and official results!")
    except:
        print("FAILED! There is a difference of {} records between the processed and official results!".format(series_wos.sum() - wos_total_results))

    print('-'*74)                   # Print a cool divider

    # # Assertions about the individual years
    for key in dict_real_wos:
        try:
            assert(dict_real_wos[key] == series_wos[key])
            print("SUCCESS! the year {} seems to be fine!".format(key))
        except:
            print("FAILED! The year {} got a difference of {} between the processed and official results".format(key, series_wos[key] - dict_real_wos[key]))

    print('-'*74)                   # Finish with my cool divider