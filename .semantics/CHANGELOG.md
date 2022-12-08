# 1.0.0 (2022-12-08)


### Bug Fixes

* add utf-8 encoding when opening text file. ([6f6f986](https://github.com/PeterWJefferson/CourseProject/commit/6f6f986ac41991e7e4a35ff59d31a1c8c91947da))
* cleans up code, updates docs ([10240d8](https://github.com/PeterWJefferson/CourseProject/commit/10240d876fa616f142f47460abb6810f60e1fbcc))
* Correted the news source names from checkbox that gets sent into API since the syntax was off for some of the news orgs with spaces in them. i.e. @FoxNews was being input as fox_news. ([2aa56db](https://github.com/PeterWJefferson/CourseProject/commit/2aa56db22511e97f8a2e5103dbf9cd2d0c604ca9))
* overfitting bug removed ([a07db64](https://github.com/PeterWJefferson/CourseProject/commit/a07db64b0312c830e85fdf4fdd5de5d1b3198acf))
* re-cleans tweets after filtering search input ([8abd210](https://github.com/PeterWJefferson/CourseProject/commit/8abd210943bddfa1f31b5fb41293e782b364c1df))
* Removed upvote button/logic ([dc5e856](https://github.com/PeterWJefferson/CourseProject/commit/dc5e8560e59c49a8d18ddfeb77f6d9a30a191d60))


### Features

* Add Progress Report ([f012e45](https://github.com/PeterWJefferson/CourseProject/commit/f012e45b1e2ea77420dca7b3daf2e2c17b2c2c55))
* added delete lines functionality to delete all but 31 documents from the corpus when the "Click to delete previous searches" button is clicked on the home page. ([e2e3bd8](https://github.com/PeterWJefferson/CourseProject/commit/e2e3bd84fb34e96dc4b4dddeab1111960863c89d))
* Added delete recent search topic button to index.html, and back button and homepage UIUC logo to results.html. Created delete_search_topic() function to hold functionality to delete all the recent topics stored. ([f1f9f0a](https://github.com/PeterWJefferson/CourseProject/commit/f1f9f0a1a2a3f11e4c0a8f49b58578c57214df4a))
* added hyperlinking to each tweet result ([730334b](https://github.com/PeterWJefferson/CourseProject/commit/730334b79986cec9f5c5aefbc814f0a402567c5a))
* Added logic to route returned tweets to the results.html page. ([6c784f7](https://github.com/PeterWJefferson/CourseProject/commit/6c784f7144128b35d951b9e1d5fbceb243971106))
* Added new CSS styling ([8a229ef](https://github.com/PeterWJefferson/CourseProject/commit/8a229ef3fb7f8cee6a94fefd8ab95e0e278eb747))
* Added news source check boxes to search page and linked them to the backend to search those news sources only for the query if any of the boxes are selected. ([eca7977](https://github.com/PeterWJefferson/CourseProject/commit/eca797759a10e6e5749016981778ccf6789043bb))
* added percentage printout on results page of each sentiment by news source selected. ([2135947](https://github.com/PeterWJefferson/CourseProject/commit/2135947a93b9835981d0d25ba669458b734e4f89))
* added recent corpus and filter recent searches in corpus ([04d125f](https://github.com/PeterWJefferson/CourseProject/commit/04d125f8d636b94658ad53672bd38f6b6d55736e))
* added Recommended search topic buttons that populate the search bar when clicked. Also added recommended search skeleton for backend to use PLSA. Added title header and UIUC Logo. ([3cac386](https://github.com/PeterWJefferson/CourseProject/commit/3cac386b7a1371ce93bf7edcc21a803348d19108))
* added Recommended search topic buttons that populate the search bar when clicked. Also added recommended search skeleton for backend to use PLSA. Added title header and UIUC Logo. ([f210a48](https://github.com/PeterWJefferson/CourseProject/commit/f210a488dc3c42c930bdda9703098bfc2bdf371a))
* Added upvote button to each tweet row and logic to call the upvote_post() function on backend. ([2369342](https://github.com/PeterWJefferson/CourseProject/commit/2369342de92f4954e10e49b4f56405452dab0bd2))
* adds range to subjectivity score ([8f5044c](https://github.com/PeterWJefferson/CourseProject/commit/8f5044cf899388abafa166b8e0a048524b59a717))
* adds ranker ([dbb1560](https://github.com/PeterWJefferson/CourseProject/commit/dbb1560026587724c9bfee168764ec7d4232561b))
* adds source to response ([4ceb9ae](https://github.com/PeterWJefferson/CourseProject/commit/4ceb9aeed89fd0043d4c8d2fa84cc4b3651ef4b8))
* adds tweets to persistent corpus and results for q='Thanksgiving' ([d9ae149](https://github.com/PeterWJefferson/CourseProject/commit/d9ae14948984d35c4ee60b073a1de55a206f1d7b))
* changes to full-length tweets ([fb2c0df](https://github.com/PeterWJefferson/CourseProject/commit/fb2c0df22be7382d4978b16a6b477c628598e41b))
* changes to full-length tweets ([01fb3ce](https://github.com/PeterWJefferson/CourseProject/commit/01fb3ce1f84e66d9aa83fd23e352fa8c8dfa6e65))
* Cleaned up news source sentiment percetage print out on results page and added total number of tweets analyzied for sentiment analysis in printout. ([7407421](https://github.com/PeterWJefferson/CourseProject/commit/7407421298c6db3963c9cebb6d17ca8c0552c562))
* connects the API to the Twitter client functions ([c955f56](https://github.com/PeterWJefferson/CourseProject/commit/c955f56fd2f2c52dadb17474dcaa18a400e998e3))
* Created initial frontend files, added search bar and POST button that stores user query and jumps to the results page. Re-ordered file structure to get Flask frontend files to reference correctly via flask documentation: https://flask.palletsprojects.com/en/2.2.x/quickstart/#static-files ([7f861d1](https://github.com/PeterWJefferson/CourseProject/commit/7f861d1db9c8500222f356218d92696893f8dc21))
* Hyperlinked the Twitter accounts in the Account columns ([c24085d](https://github.com/PeterWJefferson/CourseProject/commit/c24085dbf66e4a6251c15191d671a69c714cd4e8))
* **news:** news tweets function works in api.py, had trouble with app.py ([f354776](https://github.com/PeterWJefferson/CourseProject/commit/f35477614f55fe01da4361c0696760f6a0f81201))
* **news:** received news tweets from query instead of any tweets ([2d8faec](https://github.com/PeterWJefferson/CourseProject/commit/2d8faec218418744307183d9467c417656c289a1))
* Now returning subjectivity along with sentiment for each tweet. Printing out subjectivity per tweet and average per news source if selected. Color coded high vs. low sentiment values at a threshold of < 0.35 Green (good) and > 0.35 Red (bad). ([38d0a17](https://github.com/PeterWJefferson/CourseProject/commit/38d0a17197838d49bce9f3718161e640de4a7e1b))
* plsa algorithm, gets topics at /tweets/topics ([404ef8e](https://github.com/PeterWJefferson/CourseProject/commit/404ef8eefabcecd53e27c4d8e4e61ffbe2c3b124))
* **semantics:** adds semantic release, husky, project structure, and documentation ([0cf42d4](https://github.com/PeterWJefferson/CourseProject/commit/0cf42d4959366626a95e6e5a8b97207305c21c95))
* sentiment analysis ([519f70f](https://github.com/PeterWJefferson/CourseProject/commit/519f70f458feedf4feabb7a9d850a4921c103b9a))
* **tweepy:** adds sample api and retrieves multiple news source tweets ([719a09a](https://github.com/PeterWJefferson/CourseProject/commit/719a09a5bd23fb1d0bc77e7c23c1b563afd8556e))
* Update display page table to prettier table that is filterable and has search, and pagination. ([6f4c6ec](https://github.com/PeterWJefferson/CourseProject/commit/6f4c6ec917e42841ed10c7e2f9b869255fec070e))


### Performance Improvements

* improves plsa runtime by using random sampling instead of entire corpus ([e37a90c](https://github.com/PeterWJefferson/CourseProject/commit/e37a90cc3ee71b7c567c0c9a0fab4df79108cba6))
