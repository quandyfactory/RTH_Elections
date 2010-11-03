#!/usr/local/bin/python
# coding: utf-8

import os, sys
sys.path.insert(0, os.path.abspath(__file__).replace('/pages.py', ''))
import config as c
sys.path.extend(c.SYSPATH)

import web
import quandy as quandy
html = quandy.Html()
tools = quandy.Tools()
import config as c
import sql as sql
import templates as t
from markdown2 import markdown
import datetime
import re
import urllib
import pytoc
from functions import *


def get_api_page(path):
    """
    Returns JSON output from the site API.
    """
    output = { 'ok': True, }

    try: page = path[1]
    except: page = ''

    if page == '':
        elections = get_elections(type='api')
        output['elections'] = elections

    elif page == 'results':
        output = get_api_results_page(path)
        return output

    elif page == 'election':
        try: election_id = int(path[2])
        except: election_id = 0

        try: ward = tools.friendly_name(path[3])
        except: ward = ''

        if election_id == 0:
            output['ok'] = False
            output['error'] = '"%s" is not a valid election ID.' % path[2]
            return output

        details = get_election_details(election_id, type='api')
        output['details'] = details
        candidates = get_candidates(election_id, ward=ward, type='api')
        output['candidates'] = candidates
        questions = get_questions(election_id, type='api')
        output['questions'] = questions
        wards = get_wards(election_id, type='api')
        output['wards'] = wards
        articles = get_articles(election_id, 'article')
        output['articles'] = articles
        blogs = get_articles(election_id, 'blog')
        output['blogs'] = blogs
        apps = get_apps(election_id)
        output['apps'] = apps

    elif page == 'candidate':
        try: candidate_id = int(path[2])
        except: candidate_id = 0
        try: election_id = int(path[3])
        except: election_id = 0
        if candidate_id == 0:
            output['ok'] = False
            output['error'] = '"%s" is not a valid candidate ID.' % path[2]
            return output
        if election_id == 0:
            output['ok'] = False
            output['error'] = '"%s" is not a valid election ID.' % path[3]
            return output

        details = get_candidate_details(election_id, candidate_id, type='api')
        output['details'] = details
        responses = get_candidate_responses(election_id, candidate_id, type='api')
        output['responses'] = responses

    elif page == 'question':
        try: question_id = int(path[3])
        except: question_id = 0
        if question_id == 0:
            output['ok'] = False
            output['error'] = '"%s" is not a valid question ID.' % path[2]
            return output
        try: election_id = int(path[2])
        except: election_id = 0
        if election_id == 0:
            output['ok'] = False
            output['error'] = '"%s" is not a valid election ID.' % path[3]
            return output
        details = get_question_details(question_id, type='api')
        output['details'] = details
        responses = get_responses(election_id, question_id, type='api')
        output['responses'] = responses
        non_responses = get_non_responses(election_id, question_id, type='api')
        output['non_responses'] = non_responses

    return output



def get_api_results_page(path):
    """
    Returns election results
    """
    output = { 'ok': True, }

    # get second tier
    try: page = path[2]
    except: page = ''

    # get ward if applicable
    try: ward = tools.friendly_name(path[4])
    except: ward = ''

    election_id = 0
    try: election_id = int(page)
    except: pass

    if page == '' and election_id > 0: # base results page, return links to reports
        reports = []
        reportlist = 'summary details polls wards data'.split(' ')
        for r in reportlist:
            reports.append({
                'report': '%s' % tools.friendly_name(r),
                'url': '%s/api/results/%s/%s' % (c.SITE_DOMAIN, r, election_id)
            })
        output['reports'] = reports

        return output

    try: election_id = path[3]
    except: pass

    if page == '':
        elections = get_elections(type='api')
        output['elections'] = elections

        return output

    elif page == 'summary':
        output['summary'] = get_results_summary(election_id, ward)

        return output

    elif page == 'details':
        output['details'] = get_results_details(election_id, ward)

        return output



    return output



def get_wards_page(path):
    """
    Returns ward maps.
    """
    section = 'Elections'
    title = 'Ward Maps'
    description = 'Google Map showing the ward boundaries.'
    output = []
    addline = output.append

    addline("""
        <div class="centered">
        <iframe width="605" height="450" frameborder="0" scrolling="no"
        marginheight="0" marginwidth="0"
        src="http://maps.google.ca/maps/ms?msa=0&amp;cd=2&amp;sll=43.414317,-79.758036&amp;sspn=0.680053,1.407282&amp;hl=en&amp;ie=UTF8&amp;t=h&amp;msid=110606866639509831986.00047974ab2ae164c6984&amp;ll=43.282204,-79.93309&amp;spn=0.361403,0.54863&amp;output=embed"></iframe><br
        /><small>View <a
        href="http://maps.google.ca/maps/ms?msa=0&amp;cd=2&amp;sll=43.414317,-79.758036&amp;sspn=0.680053,1.407282&amp;hl=en&amp;ie=UTF8&amp;t=h&amp;msid=110606866639509831986.00047974ab2ae164c6984&amp;ll=43.282204,-79.93309&amp;spn=0.361403,0.54863&amp;source=embed"
        style="color:#0000FF;text-align:left">City of Hamilton Ward Boundaries</a>
        in a larger map</small>
        </div>
        """
    )

    template = t.default
    template = template.replace('[[date]]', get_date())
    template = template.replace('[[time]]', get_time())
    template = template.replace('[[title]]', title)
    template = template.replace('[[section]]', section)
    template = template.replace('[[description]]', description)
    template = template.replace('[[content]]', '\n'.join(output))
    return title, template


def get_apidoc_page(path):
    """
    Returns API Documentation.
    """
    section = 'Site Notes'
    title = 'API Documentation'
    description = 'Documentation on how to use the RTH Elections API.'
    output = []
    addline = output.append

    query = sql.text("""
        select content, last_updated
        from election_apidoc
        order by doc_id desc
        limit 1
        """, bind=sql.engine
    )
    rs = query.execute().fetchall()
    if len(rs) == 0:
        addline('Sorry, but the API documentation is not currently available.')

    else:
        addline(rs[0].content)
        addline('\n*Last Updated: %s*' % (rs[0].last_updated))
        content = markdown('\n'.join(output))
        toc = pytoc.Toc(html_in=content)
        toc.make_toc()
        full_content = '%s\n%s' % (toc.html_toc, toc.html_out)

    template = t.default
    template = template.replace('[[date]]', get_date())
    template = template.replace('[[time]]', get_time())
    template = template.replace('[[title]]', title)
    template = template.replace('[[section]]', section)
    template = template.replace('[[description]]', description)
    template = template.replace('[[content]]', full_content)
    return title, template




def get_elections_page(path):
    """
    Returns a default page with a list of links to elections
    """
    section = 'Elections'
    title = 'Elections'
    description = 'Main elections page, where you can choose which election to follow.'

    output = []
    addline = output.append
    elections = get_elections()

    if len(elections) > 0:
        addline('<p>Choose an election to explore:</p>')
        addline('<ul>')
        for row in elections:
            addline('<li><a href="%s">%s</a></li>' % (row['url'], row['title']))
        addline('</ul>')

    template = t.default
    template = template.replace('[[date]]', get_date())
    template = template.replace('[[time]]', get_time())
    template = template.replace('[[title]]', title)
    template = template.replace('[[section]]', section)
    template = template.replace('[[description]]', description)
    template = template.replace('[[content]]', '\n'.join(output))
    return title, template


def get_election_page(path):
    """
    Returns a page for a given election
    """
    output = []
    addline = output.append

    section = 'Elections'
    title = 'Elections'
    description = 'Details for an election.'

    try: election_id = path[1]
    except: election_id = 0

    try: ward = tools.friendly_name(path[2])
    except: ward = ''

    if election_id == 0:
        return get_default_page(path)


    details = get_election_details(election_id)

    if len(details) == 0:
        addline('<p class="red">That does not appear to be a valid election.</p>')

    else:
        title = '%s %s (%s)' % (details['election'], ward.replace(' 0', ' ') if ward != '' else '', details['type'])

        description = 'List of candidate details and questions for %s' % (details['election'])

        addline('<p><strong>Note to Candidates:</strong> We make every attempt to ensure that the information provided here is correct. If you notice that any information about you is incorrect or missing, please <a href="mailto:editor@raisethehammer.org">let us know</a> and we will fix it.</p>')

        addline('<h3>In This Page:</h3>')
        addline('<ul>')
        addline('<li><a href="#questions">Campaign Questions</a></li>')
        addline('<li><a href="#candidates">Candidates</a></li>')
        addline('<li><a href="#articles">RTH Articles</a></li>')
        addline('<li><a href="#blogs">RTH Blog Entries</a></li>')
        addline('<li><a href="#apps">Known Third-Party Apps</a></li>')
        addline('</ul>')

        addline('<h3><a name="questions"></a>Campaign Questions (<a href="#">top</a>)</h3>')
        addline('<p>Click on a question to see the responses from the candidates.</p>')
        questions = get_questions(election_id, ward=ward)
        if len(questions) == 0:
            addline('<p class="red">There do not appear to be any questions for this election yet.</p>')
        else:
            addline('<ul>')
            for row in questions:
                addline('<li><a title="See candidate responses to this question" href="%s">%s</a></li>' % (row['url'], row['question']))
            addline('</ul>')

        addline('<h3><a name="candidates"></a>Candidates (<a href="#">top</a>)</h3>')

        candidates = get_candidates(election_id, ward=ward)
        if len(candidates) == 0:
            addline('<p class="red">There do not appear to be any candidates for this election yet.</p>')
        else:
            addline('<table>')

            addline('<tbody>')
            thisward = ''
            for row in candidates:
                thatward = thisward
                thisward = row['ward']
                if thisward != thatward:
                    addline('<tr><th class="section_header" colspan="6">')
                    addline('<a title="See only %s" href="/election/%s/%s">%s</a></th></tr>' % (
                        thisward.replace(' 0', ' '),
                        election_id,
                        tools.unfriendly_name(thisward),
                        thisward.replace(' 0', ' ')
                        )
                    )
                    addline('<tr><th>Name</th><th>Votes</th><th>Email</th><th>Website</th><th>Phone</th></tr>')

                this_class, this_title = '', ''
                if row['withdrawn'] == 1:
                    this_class = 'withdrawn'
                    this_title = '%s has withdrawn from the election' % (get_straight_name(row['name']))

                addline('<tr class="%s" title="%s">' % (this_class, this_title))
                addline('<td style="white-space: nowrap"><a title="See details for %s" href="%s">%s</a></td>' % (row['name'], row['url'], row['name']))
                addline('<td>%s</td>' % (row['votes']))
                if row['email'] != '':
                    addline('<td><a href="mailto:%s">%s</a></td>' % (row['email'], row['email']))
                else:
                    addline('<td>(no email listed)</td>')
                if row['website'] != '':
                    addline('<td><a href="%s">%s</a></td>' % (row['website'], row['website']))
                else:
                    addline('<td>(no website listed)</td>')
                # phone
                addline('<td style="white-space: nowrap">')
                if row['home_phone'] != '':
                    addline('%s (home)<br>' % (row['home_phone']))
                if row['bus_phone'] != '':
                    addline('%s (bus)<br>' % (row['bus_phone']))
                if row['fax_number'] != '':
                    addline('%s (fax)<br>' % (row['fax_number']))
                addline('</td>')
                addline('</tr>')
            addline('</tbody></table>')
            if ward != '':
                addline('<p><a href="/election/%s">&larr; Back to Election page</a></p>' % (election_id))

        addline('<h3><a name="articles"></a>RTH Articles (<a href="#">top</a>)</h3>')

        articles = get_articles(election_id, 'article')
        for article in articles:
            addline('<p><a href="%s">%s</a>, By %s, Published %s</p>' % (
                article['url'], article['title'], article['author'], article['date_issued']
                )
            )

        addline('<h3><a name="blogs"></a>RTH Blog Entries (<a href="#">top</a>)</h3>')
        blogs = get_articles(election_id, 'blog')
        for blog in blogs:
            addline('<p><a href="%s">%s</a>, By %s, Published %s</p>' % (
                blog['url'], blog['title'], blog['author'], blog['date_issued']
                )
            )

        addline('<h3><a name="apps"></a>Known Third-Party Apps (<a href="#">top</a>)</h3>')
        apps = get_apps(election_id)
        if len(apps) > 0:
            addline('<ul>')
            for app in apps:
                addline('<li><a href="%s">%s</a></li>' % (app['url'], app['title']))
            addline('</ul>')
        else:
            addline('<p class="red">There do not appear to be any known third-party apps for this election.</p>')

    template = t.default
    template = template.replace('[[date]]', get_date())
    template = template.replace('[[time]]', get_time())
    template = template.replace('[[title]]', title)
    template = template.replace('[[section]]', section)
    template = template.replace('[[description]]', description)
    template = template.replace('[[content]]', '\n'.join(output))
    return title, template



def get_question_page(path):
    """
    Returns a details page for a question and an election_id
    """
    section = 'Elections'
    title = 'Question'
    description = 'Details for an election question.'

    output = []
    addline = output.append

    try: election_id = path[1]
    except: election_id = 0

    try: question_id = path[2]
    except: question_id = 0

    try: ward = tools.friendly_name(path[3])
    except: ward = ''

    if election_id == 0 or question_id == 0:
        return get_default_page(path)

    details = get_question_details(question_id)
    if len(details) == 0:
        addline('<p class="red">That does not appear to be a valid question.</p>')
    else:
        row = details[0]
        title = row['question']
        description = 'Responses to the question: "%s"' % (row['question'])

    addline('<p><a href="/election/%s/%s">&larr; Back to Election Page</a></p>' % (election_id, tools.unfriendly_name(ward)))

    addline('<h3>In This Page:</h3>')
    addline('<ul>')
    addline('<li><a href="#responses">Candidate Responses</a></li>')
    addline('<li><a href="#summary">Response Summary</a></li>')
    addline('<li><a href="#noresponse">Candidates Who Have Not Responded</a></li>')
    addline('</ul>')

    responses = get_responses(election_id, question_id, ward=ward)
    non_responses = get_non_responses(election_id, question_id, ward=ward)
    responses_count = len(responses)
    non_responses_count = len(non_responses)

    addline('<h3><a name="responses"></a>%s Candidate Response%s (<a href="#">top</a>)</h3>' % (responses_count, tools.single_or_plural(responses_count),))

    brief = {
        'Yes': 0,
        'No': 0,
        'Maybe': 0
    }

    if len(responses) == 0:
        addline('<p class="red">There do not appear to be any responses yet.</p>')
    else:
        thisward = ''
        addline('<table><tbody>')

        for row in responses:
            thatward = thisward
            thisward = row['ward']
            if thisward != thatward:
                addline('<tr><th class="section_header" colspan="3">%s</th></tr>' % (thisward))
                addline('<tr><th>Candidate</th><th>Brief Response</th><th>Full Response</th></tr>')
            addline('<tr>')
            addline('<td style="white-space: nowrap"><a href="/candidate/%s/%s/%s">%s</a></td>' % (
                row['candidate_id'], election_id, tools.unfriendly_name(row['name']), row['name'])
            )
            addline('<td>%s</td>' % (row['brief_response']))

            if row['brief_response'] in brief.keys():
                brief[row['brief_response']] += 1

            addline('<td>%s</td>' % (row['full_response'].replace('\n', '<br>')))
            addline('</tr>')
        addline('</table>')


    # Response Summary

    addline('<h3><a name="summary"></a>Response Summary (<a href="#">top</a>)</h3>')

    addline('<table class="auto_width">')
    addline('<thead><tr><th>Brief Response</th><th>Count</th><th>% of Total</th></tr></thead><tbody>')
    for resp in 'Yes No Maybe'.split(' '):
        addline('<tr><th>%s</th><td>%s</td><td>%.1f&#37;</td></tr>' % (resp, brief[resp], round(brief[resp]*100.0/responses_count, 1)))
    addline('</tbody></table>')


    # Non-Responses

    addline('<h3><a name="noresponse"></a>%s Candidate%s Ha%s Not Responded (<a href="#">top</a>)</h3>' % (
        non_responses_count,
        tools.single_or_plural(responses_count),
        tools.single_or_plural(responses_count, single_string='s', plural_string='ve'),
        )
    )

    if len(non_responses) == 0:
        addline('<p class="green">Every candidate has responded to this question.</p>')
    else:
        thisward = ''
        addline('<table><tbody>')

        for row in non_responses:
            thatward = thisward
            thisward = row['ward']
            if thisward != thatward:
                addline('<tr><th class="section_header" colspan="3">%s</th></tr>' % (thisward))
            addline('<tr>')
            addline('<td style="white-space: nowrap"><a href="/candidate/%s/%s/%s">%s</a></td>' % (row['candidate_id'], election_id, tools.unfriendly_name(row['name']), row['name']))
            addline('</tr>')
        addline('</table>')

    template = t.default
    template = template.replace('[[date]]', get_date())
    template = template.replace('[[time]]', get_time())
    template = template.replace('[[title]]', title)
    template = template.replace('[[section]]', section)
    template = template.replace('[[description]]', description)
    template = template.replace('[[content]]', '\n'.join(output))
    return title, template


def get_candidate_page(path):
    """
    Returns a details page for a candidate
    """
    section = 'Elections'
    title = 'Elections'
    description = 'Details page for this candidate.'

    output = []
    addline = output.append

    try: candidate_id = path[1]
    except: candidate_id = 0

    try: election_id = path[2]
    except: election_id = 0

    if candidate_id == 0 or election_id == 0:
        return get_default_page(path)

    addline('<h3>In This Page:</h3>')
    addline('<ul>')
    addline('<li><a href="#details">Candidate Details</a></li>')
    addline('<li><a href="#responses">Responses to Questions</a></li>')
    addline('</ul>')

    addline('<h3><a name="details"></a>Candidate Details (<a href="#">top</a>)</h3>')

    details = get_candidate_details(election_id, candidate_id)
    if len(details) > 0:
        row = details
        name = get_straight_name(row['name'])

        title = '%s, Candidate for %s' % (name, row['ward'].replace(' 0', ' '))
        addline('<table class="vertical">')
        addline('<tbody>')
        addline('<tr><th>Name</th><td><strong>%s</strong></td></tr>' % (row['name']))
        addline('<tr><th>Election</th><td><a href="/election/%s">%s</a></td></tr>' % (row['election_id'], row['election']))
        addline('<tr><th>Ward</th><td>%s</td></tr>' % (row['ward']))
        addline('<tr><th>Votes</th><td>%s</td></tr>' % (row['votes']))
        addline('<tr><th>Email</th>')
        if row['email'] != '':
            addline('<td><a href="mailto:%s">%s</a></td>' % (row['email'], row['email']))
        else:
            addline('<td>(no email listed)</td>')
        addline('</tr>')
        addline('<tr><th>Website</th>')
        if row['website'] != '':
            addline('<td><a href="%s">%s</a></td>' % (row['website'], row['website']))
        else:
            addline('<td>(no website listed)</td>')
        addline('</tr>')
        addline('<tr><th>Home</th><td>%s</td></tr>' % (row['home_phone']))
        addline('<tr><th>Business</th><td>%s</td></tr>' % (row['bus_phone']))
        addline('<tr><th>Fax</th><td>%s</td></tr>' % (row['fax_number']))
        if row['bio'] != '':
            addline('<tr><th>Bio</th><td>%s</td></tr>' % (row['bio'].replace('\n', '<br>')))
        addline('</tbody>')
        addline('</table>')

        addline('<p><a href="/election/%s">&larr; Back to Candidates</a></p>' % row['election_id'])

    addline('<h3><a name="responses"></a>Responses to Questions (<a href="#">top</a>)</h3>')

    responses = get_candidate_responses(election_id, candidate_id)
    if len(responses) == 0:
        addline('<p class="red">This candidate does not appear to have responded to any questions yet.</p>')
    else:
        thisward = ''
        addline('<table>')
        addline('<thead><tr><th>Question</th><th>Brief Response</th><th>Full Response</th></tr></thead>')
        addline('<tbody>')

        for row in responses:
            addline('<tr>')
            addline('<td><a href="%s">%s</a></td>' % (row['url'], row['question']))
            addline('<td>%s</td>' % (row['brief_response']))
            addline('<td>%s</td>' % (row['full_response'].replace('\n', '<br>')))
            addline('</tr>')
        addline('</table>')

    template = t.default
    template = template.replace('[[date]]', get_date())
    template = template.replace('[[time]]', get_time())
    template = template.replace('[[title]]', title)
    template = template.replace('[[section]]', section)
    template = template.replace('[[description]]', description)
    template = template.replace('[[content]]', '\n'.join(output))
    return title, template
