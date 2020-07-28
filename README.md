# monash-unit-info-scraper

### Dependencies

* Python 3.7
* Firefox
* Selenium & Geckodriver
* Pandas

### How to use

* Consists of two scripts, unit_code_scraper.py and unit_info_scraper.py.

  #### Getting a list of unit codes

  * unit_code_scraper.py visits the [Monash 2019 Handbook - Units by Faculty](https://www3.monash.edu/pubs/2019handbooks/units/index-byfaculty.html), scrapes all the unit codes and writes them by line to a file "{faculty}.txt". 

  * The 2019 handbook is used as it is just a static page, which is easier to scrape from than the javascript mess of the 2020 handbook. So, some units may be slightly outdated. 

  * Regular expressions can then be used on these unit lists to extract particular units of interest.

    * For example, if only third year and up maths, physics and chemistry units are wanted, could use something like 

      ```bash
      egrep '^(MTH|PHS|CHM)[3-9]' sci.txt >> sci_final_years.txt
      ```

  #### Getting unit info

  * These unit lists are then used to scrape the unit coordinator details from the 2020 handbook. 

  * To run the script:

    ```bash
    python unit_info_scraper.py {unit_list}.txt 
    ```

  * Unit information will then be output into a csv file of the same name as the text file. 

  * If further sorting/extraction is required, can then use Microsoft excel to filter results using regular expressions.