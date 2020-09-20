def check_consistency(source, series, dict_real):
    """Test unit for data extraction of alll sources

        Args:
            source (str): Name of the source
            series (pandas.Series): Contains the value counts per year from the 
            extracted data
            dict_real (dict): Contains the actual observed results
    """
    total_results = sum(dict_real.values())

    print('-'*74)                   # Begin with my cool divider
    print("Testing for... {}".format(source.upper()))
    print('-'*74)                   # Print a cool divider

    # Assertions about the total counts
    try:
        assert(total_results == series.sum())
        print("SUCCESS! Total count was equal between the processed and "
            "official results!")
    except:
        print("FAILED! There is a difference of {} records between the "
            "processed and official results!".
            format(series_wos.sum() - wos_total_results))

    print('-'*74)                   # Print a cool divider

    # # Assertions about the individual years
    for key in dict_real:
        try:
            assert(dict_real[key] == series[key])
            print("SUCCESS! the year {} seems to be fine!".format(key))
        except:
            print("FAILED! The year {} got a difference of {} between the "
            "processed and official results".
            format(key, series_wos[key] - dict_real_wos[key]))

    print('-'*74)                   # Finish with my cool divider