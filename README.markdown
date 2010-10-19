## API Documentation

### Introduction

The RTH Elections API makes the content of this site available programmatically in JSON format. For now it is a read-only format, accessible via HTTP GET requests.

Every JSON object is returned in the form of a key/value dictionary, and includes an `ok` key. The `ok` key returns `true` if the request was successful and `false` if the request was unsuccessful - e.g. if you try to get an election ID that doesn't exist.

Unsuccessful requests will also include an `error` key that explains what went wrong.

#### JSON Backgrounder

JSON, or Javascript Object Notation, is a lightweight structured data format that allows you to transfer data objects across a network.

JSON supports the following data types: strings, numbers, booleans (true/false), `null`, objects, and arrays. The latter two data types are **collections**:  an array is an ordered set of values, and an object is an unordered set of keys and values. You can nest collections arbitrarily, e.g. by having an array of objects.

Among the many benefits of JSON are the following:

* It's simple.
* It's lightweight, with minimal 'boilerplate' and other overhead (especially compared to XML).
* It's human-readable.
* It's an executable subset of Javascript.
* It's easy to parse and nearly every programming language has a JSON parser library.

For these and other reasons, JSON has mostly supplanted XML as the "X" in AJAX, or asynchronous data transfer in a web page.

#### JSON in PHP

If you're using PHP version 5.2+ to develop your application, you can use the handy built-in API functions to decode the JSON object into either a native PHP object or a native PHP array.

    <$php
    $url = 'http://elections.raisethehammer.org/api/election/1';

    # fetch the data from the API page
    $response = file_get_contents($url);

    # json_decode requires PHP 5.2+

    # decode JSON object into a PHP object
    $obj = json_decode($response);

    # decode JSON object into a PHP array instead
    $arr = json_decode($response, true);

    # process and render the code
    ?>

Now that you have a native PHP data structure, you can navigate through it using PHP's own tools. Here is a [sample script](http://gist.github.com/617837) that grabs the JSON object from the API, converts it into a PHP array, and renders the contents into HTML.

### The RTH Elections API

#### Elections

The base URL for the api is:

    http://elections.raisethehammer.org/api

This returns a list of elections. Each element in the list is a dictionary object of details for that election, including the URL of the JSON page with the full details for that election.

Example output:

    {
      "ok": true,
      "elections":
      [
        {
          "url": "http://elections.raisethehammer.org/api/election/1",
          "type_id": 1,
          "type": "Municipal",
          "title": "Hamilton Municipal Election 2010"
        }
      ]
    }

#### Election Details

Each election returned in the Elections API page includes a URL for that election, e.g.

    http://elections.raisethehammer.org/api/election/1

The details page for an election includes:

* `details` - the details of the election itself;
* `candidates` - a list of candidates, with a dictionary object of details for each candidate; and
* `questions` - a list of questions that RTH has posed to the candidates.
* `wards` - a list of specific wards with a link to details for each individual ward.
* `articles` - a list of RTH articles related to the election.
* `blogs` - a list of RTH blog entries related to the election.

Each candidate object includes the URL of the details page for that candidate. Likewise, each question object includes the URL of the details page for that question.

#### Candidates

Each candidate returned in the Election Details API page includes a URL for that candidate, e.g.

    http://elections.raisethehammer.org/api/candidate/70/1

The details page for the candidate includes:

* `details` - the details of the candidate:
    - `url` (the URL of the candidate's details page in the API)
    - `ward`
    - `name`
    - `email`
    - `home_phone`
    - `bus_phone`
    - `fax_number`
    - `website`
    - `gender`
    - `bio`
    - `incumbent` (0 or 1)
    - `withdrawn`  (0 or 1)

* `responses` - a list of responses that the candidate has given to RTH election questions.

Note that each response includes the URL of the details page for the question the candidate answered.

#### Questions

Each question candidates were asked has a Question Details API page, e.g.

    http://elections.raisethehammer.org/api/question/1/1

The details page for each question includes:

* `details` - the details of the question;
* `responses` - a list of responses by candidates who responded; and
* `non_responses` - a list of candidates who have not responded.

The lists of responses and non-responses also include links back to the respective candidate pages.

#### Wards

The election details include a list of wards in the election, with a link to details for each individual ward, e.g.

    http://elections.raisethehammer.org/api/election/1/mayor

This returns the same results as the Election Details page, but the `candidates` object only includes candidates in the specified ward.

### Licence: Creative Commons Attribution-ShareAlike

<p><a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width: 0pt;" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png"></a><br>This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.</p>

We created an API because we want to share our data. All we ask is that if you use data from the RTH Elections site, please attribute the original source of this data by displaying a link to [http://raisethehammer.org](http://raisethehammer.org) or [http://elections.raisethehammer.org](http://elections.raisethehammer.org) and make your own re-distributed data available under a compatible licence.

Please [let us know](mailto:editor@raisethehammer.org?Subject=Election Data) if you build something so we can check it out and link to it.

Similarly, if you're building something and require a change to the API, additional data, etc., please [contact us](mailto:editor@raisethehammer.org?Subject=Election API Change Request) and let us know. We'll do our best to help.

### Source Code

The source code for this web application is [available on github](http://github.com/quandyfactory/RTH_Elections).
