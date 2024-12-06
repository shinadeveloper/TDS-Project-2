# Dataset Analysis Report

## Summary Statistics
|        |   book_id |   goodreads_book_id |     best_book_id |         work_id |   books_count |           isbn |         isbn13 | authors      |   original_publication_year | original_title   | title          | language_code   |   average_rating |    ratings_count |   work_ratings_count |   work_text_reviews_count |   ratings_1 |   ratings_2 |   ratings_3 |      ratings_4 |       ratings_5 | image_url                                                                                | small_image_url                                                                        |
|:-------|----------:|--------------------:|-----------------:|----------------:|--------------:|---------------:|---------------:|:-------------|----------------------------:|:-----------------|:---------------|:----------------|-----------------:|-----------------:|---------------------:|--------------------------:|------------:|------------:|------------:|---------------:|----------------:|:-----------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|
| count  |  10000    |     10000           |  10000           | 10000           |    10000      | 9300           | 9415           | 10000        |                    9979     | 9415             | 10000          | 8916            |     10000        |  10000           |      10000           |                  10000    |    10000    |    10000    |     10000   | 10000          | 10000           | 10000                                                                                    | 10000                                                                                  |
| unique |    nan    |       nan           |    nan           |   nan           |      nan      | 9300           |  nan           | 4664         |                     nan     | 9274             | 9964           | 25              |       nan        |    nan           |        nan           |                    nan    |      nan    |      nan    |       nan   |   nan          |   nan           | 6669                                                                                     | 6669                                                                                   |
| top    |    nan    |       nan           |    nan           |   nan           |      nan      |    4.39023e+08 |  nan           | Stephen King |                     nan     |                  | Selected Poems | eng             |       nan        |    nan           |        nan           |                    nan    |      nan    |      nan    |       nan   |   nan          |   nan           | https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png | https://s.gr-assets.com/assets/nophoto/book/50x75-a91bf249278a81aabab721ef782c4a74.png |
| freq   |    nan    |       nan           |    nan           |   nan           |      nan      |    1           |  nan           | 60           |                     nan     | 5                | 4              | 6341            |       nan        |    nan           |        nan           |                    nan    |      nan    |      nan    |       nan   |   nan          |   nan           | 3332                                                                                     | 3332                                                                                   |
| mean   |   5000.5  |         5.2647e+06  |      5.47121e+06 |     8.64618e+06 |       75.7127 |  nan           |    9.75504e+12 | nan          |                    1981.99  | nan              | nan            | nan             |         4.00219  |  54001.2         |      59687.3         |                   2919.96 |     1345.04 |     3110.89 |     11475.9 | 19965.7        | 23789.8         | nan                                                                                      | nan                                                                                    |
| std    |   2886.9  |         7.57546e+06 |      7.82733e+06 |     1.17511e+07 |      170.471  |  nan           |    4.42862e+11 | nan          |                     152.577 | nan              | nan            | nan             |         0.254427 | 157370           |     167804           |                   6124.38 |     6635.63 |     9717.12 |     28546.4 | 51447.4        | 79768.9         | nan                                                                                      | nan                                                                                    |
| min    |      1    |         1           |      1           |    87           |        1      |  nan           |    1.9517e+08  | nan          |                   -1750     | nan              | nan            | nan             |         2.47     |   2716           |       5510           |                      3    |       11    |       30    |       323   |   750          |   754           | nan                                                                                      | nan                                                                                    |
| 25%    |   2500.75 |     46275.8         |  47911.8         |     1.00884e+06 |       23      |  nan           |    9.78032e+12 | nan          |                    1990     | nan              | nan            | nan             |         3.85     |  13568.8         |      15438.8         |                    694    |      196    |      656    |      3112   |  5405.75       |  5334           | nan                                                                                      | nan                                                                                    |
| 50%    |   5000.5  |    394966           | 425124           |     2.71952e+06 |       40      |  nan           |    9.78045e+12 | nan          |                    2004     | nan              | nan            | nan             |         4.02     |  21155.5         |      23832.5         |                   1402    |      391    |     1163    |      4894   |  8269.5        |  8836           | nan                                                                                      | nan                                                                                    |
| 75%    |   7500.25 |         9.38223e+06 |      9.63611e+06 |     1.45177e+07 |       67      |  nan           |    9.78083e+12 | nan          |                    2011     | nan              | nan            | nan             |         4.18     |  41053.5         |      45915           |                   2744.25 |      885    |     2353.25 |      9287   | 16023.5        | 17304.5         | nan                                                                                      | nan                                                                                    |
| max    |  10000    |         3.32886e+07 |      3.55342e+07 |     5.63996e+07 |     3455      |  nan           |    9.79001e+12 | nan          |                    2017     | nan              | nan            | nan             |         4.82     |      4.78065e+06 |          4.94236e+06 |                 155254    |   456191    |   436802    |    793319   |     1.4813e+06 |     3.01154e+06 | nan                                                                                      | nan                                                                                    |

## Insights from LLM
Certainly! Here are some insights and observations derived from the provided book dataset:

### 1. **Ratings and Popularity**
   - The average rating of books ranges from approximately 3.34 (lowest) to 4.47 (highest). The overall average rating across the dataset appears to be quite high, indicating that most of these books are well-received.
   - **High-Rated Titles**: A few notable high-rated books include "*Hamilton: The Revolution*" (4.47) and "*Llama Llama Mad at Mama*" (4.28), which have garnered significant popularity based on ratings count.

### 2. **Publication Year Trends**
   - The dataset contains a mix of older classics (e.g., Agatha Christie’s 1922 title) and recent publications (e.g., books from 2016). 
   - Books from 2000s and 2010s appear to have higher ratings on average compared to earlier publications, which may indicate changing reader preferences or improved literary standards in recent years.

### 3. **Author Popularity**
   - Some authors are featured multiple times such as Agatha Christie and Dean Koontz, who have a broad range of works listed. Popular authors tend to have higher ratings and larger ratings counts.
   - Notably, some titles with collaborative authors (e.g., "*Beautiful Chaos*" by Kami Garcia and Margaret Stohl) also receive substantial ratings and reviews.

### 4. **Genres and Language**
   - While the dataset includes primarily English titles (with some in Spanish), this suggests a market focus on English-speaking demographics which could impact the diversity and reach of the books. 
   - The diversity of genres cannot be determined directly from the data, but titles suggest a mix of fiction, non-fiction, fantasy, and mystery genres, indicating various reader interests.

### 5. **Ratings Distribution**
   - The dataset includes detailed ratings breakdowns (from ratings 1 to 5). 
   - Analyzing this could provide insights into reader satisfaction beyond the average rating. For instance, titles with a high count of 5-star ratings but low overall ratings might indicate polarized opinions.

### 6. **Illustrative Titles and Cover Arts**
   - Several titles in the dataset have compelling cover arts, particularly notable for attracting younger audiences or in the children's literature segment (e.g., little golden books).
   - Books like "*Pippi in the South Seas*" (Pippi Långstrump i Söderhavet) show cultural impact, being translated and adapted into different languages and formats.

### 7. **Image URLs**
   - The presence of image URLs alongside books indicates that visual appeal might correlate with higher ratings, as readers often first judge a book by its cover.

### 8. **Variability of Ratings Count**
   - Notable variability in ratings count suggests that newer or more popular books receive significantly more attention. For example, books like "*Middlesex*" have exceptionally high ratings counts (over 500,000), while others struggle to reach even 10,000. This disparity highlights the competitive nature of the book market.

### Conclusion
This dataset provides a microcosm of the broader literature landscape, with valuable insights into reader preferences, publication trends, and author popularity. Further analyses could involve clustering books by rating patterns, publication year, or author trends to gain even deeper insights into consumer behavior and market dynamics.

## Visualizations
### correlation_heatmap.png
![Visualization](correlation_heatmap.png)

### scatterplot.png
![Visualization](scatterplot.png)

