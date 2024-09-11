BasketBasket Technical Interview Steps

Getting Started
1. git clone https://github.com/yourusername/technicalAssessment.git
2. cd technicalAssessment
3. python -m venv env
4. source env/bin/activate
5. pip install -r requirements.txt
6. python src/main.py 
7. Add “grocery_store_a.json” and “grocery_store_b.json” to “src/data/grocery_items_raw” (please create folder, Github won’t host empty folder)

Future considerations
- Data integrity / deeper understanding
    - E.g. Store A “Yaucono Cafe Instant Regular 3.6 oz” has a unit price of “$2.34/oz” but a current price of $4.22. Further understanding of data on a case by case basis may be required
    - E.g. Store A “Famosito Fruit Punch” has a unit price of “$0.43 / fl oz”. The dataset may need specific cases / review as density is required to convert this amount to ounces  
- Extracting new key value pairs from name
    - Brand name, variant, product counts, and product type
- Fuzzy match execution time
    - Reduce iteration complexity, currently O(n^2), by creating internal betterBasketIDs that can identity and group categories and product types. This would allow the vectorized operations to skip items that shouldn’t match.
    - Writing results in batches to save memory 
- Outlier range
    - Standard deviations should be considered when analyzing the price / unit price difference of products. Prices that are too far outside of the range likely indicate that the products being compared are in fact not the same.
- Normalized labels
    - Increase faith the unit price comparisons are accurate. This would likely involve an internal dictionary created by BetterBasket. This is the same for categories, which would greatly increase the likelihood of proper comparisons.
- Code refactoring
    - Some aspects of this code can be refactored to be made more reusable (e.g. file reads and writes) 

Part I: Exploring the problem
- Data is not normalized across the grocery industry and amongst competing grocers 
- Grocers want to understand their competitor prices in real-time to make strategic decisions
- Understanding differences in prices amongst similar / same products will allow grocers to compete effectively  

Part II: Understanding the data
Store A:
1. Created a util called “json_keys_util.py” to return all the unique keys in Grocery Store A’s dataset
2. Upon review of Grocery Store A’s keys, I concluded that I should look for any nested keys in Grocery Store A’s dataset to better understand the data. I created a util called “nested_json_keys_util.py” to better understand Grocery Store A’s data. The script returns the following unique keys: ['seoItemMetaData', 'product', 'contentLayout', 'reviews', 'idml']
3. Upon a quick visual inspection, the product key looked promising. I created a new util called “store_a_key_extractor_util.py”. The data found was promising. Key filters were introduced to only return relevant information and the results were saved to the “grocery_items_clean” folder for further manipulation and review.

Store B
1. Similar to Store A, I began by exploring the keys in Grocery Store B’s dataset. Upon observation an html data structure, I leveraged an html parser, BeautifulSoup, to extract the HTML.
2. In order to review effectively, I only returned index 0 of Grocery Store B’s data. It was evident that the grocery data may be buried in html tags, but could also be in the script tag. I tested this assumption and validated that this was true, helping remove the burden of going through the entire html document to find the necessary data.
3. The data in the script data was extracted and cleaned to be saved as json. The relevant keys were identified and the products were mapped to be saved to the “grocery_items_clean” folder for further manipulation and review. 

Part III: Normalizing the data
- Review of Grocery Store A & B’s data indicated that we can extract and normalize product names, prices, categories, and variants.

Store A:
1. Looped through Grocery Store A’s products to normalize individual product data. Grocery Store A provided price and unitPrices, variant information, and up to 4 levels of categories. Parsers were introduced to separated some of this data into its own key value pairs. The normalized data was saved to the “grocery_items_normalized” folder for comparative analysis with Grocery Store B.

Store B:
1. The data at Grocery Store B has a little less structure, including item count in the name and variants that include the amount and the label. Additionally, the categories and other fields are in Spanish. 
2. The first challenge was to separate the variant information to determine unit pricing. Various string parsers were introduced to get the necessary data separated. I also tracked the labels found throughout this dataset to make sure processing was being executed properly. Special use cases were introduced as well (e.g. “por peso” was changed to “by weight”).
3. Other values were reformatted to be numbers or strings with the relevant information.
4. Categories were translated from Spanish to English to augment data comparison in the future.
5. Note: Attempts to extract the relevant count information were made, but given the more manual process of reviewing relevant labels in the product names, this process was halted. With more time invested, there is a way to get the new of items associated with the product (e.g. a 6 pack of soap) in order to get the accurate unit price.
6. The normalized data was saved to the “grocery_items_normalized” folder for comparative analysis with Grocery Store A.

Part IV: Comparing the data
1. Created a util “fuzzy_match_price_difference_util.py” to compares the products name, item variant, and categories to find the best matches. All results with fuzzy match scores greater than 60 are returned, including data for comparison, such as name, price, unit price, categories, price discrepancies, and score. 
2. Given the data size and execution time, new strategies were introduced to process our dataset faster, including preprocessing strings, parallel processing, and vectorized operations. JSON files were converted to CSV to reduce memory requirements and file sizes.
3. It appears that some item unit prices are in pounds and others ounces, a simple conversion was created to address this mismatch.
4. Created a util “score_unit_price_difference_analysis_util.py” that dynamically returns the best matched items and then sorts them by price difference to solve the problem [“To validate their pricing strategy, Grocery Store C needs to identify the largest pricing discrepancies between Grocery Store A and Grocery Store B for items that both stores carry.”].

Part V: Reviewing the results
1. Given limitations on comparing the total price of products, as there are chances that the products are different sizes or flavors, it is clear the unit prices should be analyzed. While outliers may still exist, larger discrepancies are easy to identify and explore further.
2. Extracting brand name, variant, product counts, and product type from the name and using in our fuzzy match would likely increase our match scores. Internal BetterBasket IDs and lists should be applied to help identify and extract this information.
3. Match score cutoffs should be considered. As the cutoff score approaches 0, the reliability of the fuzzy matches goes down. As most scores were between 20 and 45, and matches between 45 and 60 appeared too unreliable, a cutoff of 60 was used to return any potential matches. A second store cutoff to compare product unit prices was introduced to allow for clearer results.
