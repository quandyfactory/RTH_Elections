#!/usr/local/bin/python
# coding: utf-8

import os, sys
sys.path.insert(0, os.path.abspath(__file__).replace('/functions.py', ''))
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
                    addline('<tr><th>Name</th><th>Email</th><th>Website</th><th>Phone</th></tr>')
                
                this_class, this_title = '', ''
                if row['withdrawn'] == 1:
                    this_class = 'withdrawn'
                    this_title = '%s has withdrawn from the election' % (get_straight_name(row['name']))

                addline('<tr class="%s" title="%s">' % (this_class, this_title))
                addline('<td style="white-space: nowrap"><a title="See details for %s" href="%s">%s</a></td>' % (row['name'], row['url'], row['name']))
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


def get_straight_name(name):
    """
    Takes a `Lastname, Firstname` string and returns a `Firstname Lastname` string
    """
    namelist = name.split(',')
    namelen = len(namelist)
    outname = []
    for i in range(namelen): outname.append(namelist[namelen-i-1].strip())
    return ' '.join(outname)


def get_date():
    """
    Returns a formatted date
    """
    months = ' January February March April May June July August September October November December'.split(' ')
    weekdays = 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split(' ')
    today = datetime.datetime.today()
    return '%s. %s %s, %s' % (weekdays[today.weekday()], months[today.month], today.day, today.year)



def get_time():
    """
    Returns a formatted time
    """
    an_hour = datetime.timedelta(seconds=60*60)

    today = datetime.datetime.today()
    today = today + an_hour

    hour = today.hour
    if hour > 12:
        ampm = 'PM'
        hour = hour-12
    elif hour == 12:
        ampm = 'PM'
    else:
        ampm = 'AM'
    return '%s:%02d %s' % (hour, today.minute, ampm)



def get_stub(type):
    """
    Returns an url stub for data output.
    """
    return '' if type == 'web' else '%s/api' % c.SITE_DOMAIN



def get_elections(type='web'):
    """
    Returns a list of elections
    """

    stub = get_stub(type)

    query = sql.text("""
        select e.election_id, e.election, t.type_id, t.type
        from elections e
        inner join election_types t
        on e.type_id = t.type_id
        order by e.election_id desc
        """, bind=sql.engine
    )
    rs = query.execute().fetchall()

    if len(rs) == 0: return []

    elections = []
    for row in rs:
        elections.append({
            'url': '%s/election/%s' % (stub, row.election_id),
            'title': row.election,
            'type': row.type,
            'type_id': row.type_id,
        })

    return elections



def get_wards(election_id, type='web'):
    """
    Returns a list of wards
    """

    stub = get_stub(type)

    query = sql.text("""
        select
        distinct(c.ward),
        count(c.candidate_id) as candidates,
        e.election
        from election_candidates c
        inner join elections e
        on c.election_id = e.election_id
        where c.election_id = :election_id
        group by c.ward
        order by c.ward
        """, bind=sql.engine
    )
    rs = query.execute(election_id=election_id).fetchall()
    if len(rs) == 0: return {}
    wards = []
    for row in rs:
        wards.append(
            {
                'ward': row.ward,
                'candidates': row.candidates,
                'election': row.election,
                'url': '%s/election/%s/%s' % (stub, election_id, tools.unfriendly_name(row.ward)),
            }
        )
    return wards


def get_election_details(election_id, type='web'):
    """
    Returns the details for an election
    """

    stub = get_stub(type)

    query = sql.text("""
        select e.election, e.type_id, t.type
        from elections e
        inner join election_types t
        on e.type_id = t.type_id
        where election_id = :election_id
        """, bind=sql.engine
    )
    rs = query.execute(election_id=election_id).fetchall()
    if len(rs) == 0: return {}
    row = rs[0]
    return {
        'election': row.election,
        'type_id': row.type_id,
        'type': row.type,
    }



def get_candidates(election_id, type='web', ward=''):
    """
    Returns a list of candidates
    """

    stub = get_stub(type)

    if ward == '':
        query = sql.text("""
            select * from election_candidates
            where election_id = :election_id
            order by ward, name
            """, bind=sql.engine
        )
        rs = query.execute(election_id=election_id).fetchall()
    else:
        query = sql.text("""
            select * from election_candidates
            where election_id = :election_id
            and ward = :ward
            order by ward, name
            """, bind=sql.engine
        )
        rs = query.execute(election_id=election_id, ward=ward).fetchall()

    if len(rs) == 0: return []

    candidates = []
    for row in rs:
        candidates.append({
            'url': '%s/candidate/%s/%s' % (stub, row.candidate_id, election_id),
            'candidate_id': row.candidate_id,
            'ward': row.ward,
            'name': row.name,
            'address': row.address if row.address is not None else '',
            'email': row.email if row.email is not None else '',
            'home_phone': row.home_phone if row.home_phone is not None else '',
            'bus_phone': row.bus_phone if row.bus_phone is not None else '',
            'fax_number': row.fax_number if row.fax_number is not None else '',
            'election_id': row.election_id,
            'website': row.website if row.website is not None else '',
            'bio': row.bio if row.bio is not None else '',
            'gender': row.gender if row.gender is not None else '',
            'incumbent': row.incumbent,
            'withdrawn': row.withdrawn,
        })
    return candidates


def get_candidate_details(election_id, candidate_id, type='web'):
    """
    Returns the details for a candidate
    """

    stub = get_stub(type)

    query = sql.text("""
        select c.*, e.election, t.type from election_candidates c
        inner join elections e
        on c.election_id = e.election_id
        inner join election_types t
        on e.type_id = t.type_id
        where candidate_id = :candidate_id
        """, bind=sql.engine
    )
    rs = query.execute(candidate_id=candidate_id).fetchall()
    if len(rs) == 0: return []
    row = rs[0]
    return {
        'url': '%s/candidate/%s/%s' % (stub, row.candidate_id, election_id, ),
        'name': row.name,
        'ward': row.ward,
        'address': row.address if row.address is not None else '',
        'email': row.email if row.email is not None else '',
        'home_phone': row.home_phone if row.home_phone is not None else '',
        'bus_phone': row.bus_phone if row.bus_phone is not None else '',
        'fax_number': row.fax_number if row.fax_number is not None else '',
        'election_id': row.election_id,
        'website': row.website if row.website is not None else '',
        'bio': row.bio if row.bio is not None else '',
        'election': row.election,
        'type': row.type,
        'gender': row.gender if row.gender is not None else '',
        'incumbent': row.incumbent,
        'withdrawn': row.withdrawn,
    }


def get_questions(election_id, type='web', ward=''):
    """
    Returns a list of questions for an election
    """

    stub = get_stub(type)

    query = sql.text("""
        select distinct q.question_id, r.election_id, q.question
        from election_questions q
        inner join election_responses r
        on q.question_id = r.question_id
        where r.election_id = :election_id
        order by question_id
        """, bind=sql.engine
    )
    rs = query.execute(election_id=election_id).fetchall()

    if len(rs) == 0: return []
    questions = []
    for row in rs:
        questions.append({
            'url': '%s/question/%s/%s/%s' % (stub, row.election_id, row.question_id, tools.unfriendly_name(ward) if ward != '' else ''),
            'question_id': row.question_id,
            'election_id': row.election_id,
            'question': row.question,
        })
    return questions


def get_question_details(question_id, type='web'):
    """
    Returns the details of a question
    """

    stub = get_stub(type)

    query = sql.text("""
        select distinct q.question_id, r.election_id, q.question
        from election_questions q
        inner join election_responses r
        on q.question_id = r.question_id
        where q.question_id = :question_id
        """, bind=sql.engine
    )
    rs = query.execute(question_id=question_id).fetchall()
    if len(rs) == 0:
        return []
    details = []
    row = rs[0]
    details.append({
        'url': '%s/question/%s/%s' % (stub, row.election_id, row.question_id),
        'question_id': row.question_id,
        'election_id': row.election_id,
        'question': row.question,
    })
    return details


def get_responses(election_id, question_id, type='web', ward=''):
    """
    Returns a list of responses to a question
    """

    stub = get_stub(type)

    if ward == '':
        query = sql.text("""
            select q.question_id, q.question,
            r.response_id, c.ward, c.candidate_id, c.name,
            r.brief_response, r.full_response, r.date_posted
            from election_candidates c
            inner join election_responses r
            on c.election_id = r.election_id
            and c.candidate_id = r.candidate_id
            inner join election_questions q
            on r.question_id = q.question_id
            where c.election_id = :election_id
            and r.question_id = :question_id
            and c.withdrawn != 1
            order by c.ward, c.name
            """, bind=sql.engine
        )
        rs = query.execute(election_id=election_id, question_id=question_id).fetchall()
    else:
        query = sql.text("""
            select q.question_id, q.question,
            r.response_id, c.ward, c.candidate_id, c.name,
            r.brief_response, r.full_response, r.date_posted
            from election_candidates c
            inner join election_responses r
            on c.election_id = r.election_id
            and c.candidate_id = r.candidate_id
            inner join election_questions q
            on r.question_id = q.question_id
            where c.election_id = :election_id
            and r.question_id = :question_id
            and c.ward = :ward
            and c.withdrawn != 1
            order by c.ward, c.name
            """, bind=sql.engine
        )
        rs = query.execute(election_id=election_id, question_id=question_id, ward=ward).fetchall()
    if len(rs) == 0:
        return []
    responses = []
    for row in rs:
        responses.append({
            'question_id': row.question_id,
            'question': row.question,
            'candidate_id': row.candidate_id,
            'ward': row.ward,
            'name': row.name,
            'brief_response': row.brief_response,
            'full_response': row.full_response,
            'date_posted': '%s:00' % (str(row.date_posted)[:16]) if row.date_posted != None else '',
        })
    return responses


def get_candidate_responses(election_id, candidate_id, type='web', ward=''):
    """
    Returns a list of a candidate's responses to the questions
    """

    stub = get_stub(type)

    if ward == '':
        query = sql.text("""
            select q.question_id, q.question,
            r.response_id, c.ward, c.candidate_id, c.name,
            r.brief_response, r.full_response, r.date_posted
            from election_candidates c
            inner join election_responses r
            on c.election_id = r.election_id
            and c.candidate_id = r.candidate_id
            inner join election_questions q
            on r.question_id = q.question_id
            where c.election_id = :election_id
            and r.candidate_id = :candidate_id
            order by c.ward, c.name
            """, bind=sql.engine
        )
        rs = query.execute(election_id=election_id, candidate_id=candidate_id).fetchall()
    else:
        query = sql.text("""
            select q.question_id, q.question,
            r.response_id, c.ward, c.candidate_id, c.name,
            r.brief_response, r.full_response, r.date_posted
            from election_candidates c
            inner join election_responses r
            on c.election_id = r.election_id
            and c.candidate_id = r.candidate_id
            inner join election_questions q
            on r.question_id = q.question_id
            where c.election_id = :election_id
            and r.candidate_id = :candidate_id
            and c.ward = :ward
            order by c.ward, c.name
            """, bind=sql.engine
        )
        rs = query.execute(election_id=election_id, candidate_id=candidate_id, ward=ward).fetchall()
    if len(rs) == 0:
        return []
    responses = []
    for row in rs:
        responses.append({
            'url': '%s/question/%s/%s' % (stub, election_id, row.question_id),
            'question_id': row.question_id,
            'question': row.question,
            'candidate_id': row.candidate_id,
            'ward': row.ward,
            'name': row.name,
            'brief_response': row.brief_response,
            'full_response': row.full_response,
            'date_posted': '%s:00' % (str(row.date_posted)[:16]) if row.date_posted != None else '',
        })
    return responses


def get_non_responses(election_id, question_id, type='web', ward=''):
    """
    Returns a list of non-responses to a question
    """

    stub = get_stub(type)

    if ward == '':
        query = sql.text("""
            select c.candidate_id, c.ward, c.name
            from election_candidates c
            where c.candidate_id not in (
                select c.candidate_id
                from election_candidates c
                left join election_responses r
                on c.candidate_id = r.candidate_id
                where r.question_id = :question_id
                and c.election_id = :election_id
            )
            and c.withdrawn != 1
            order by c.ward, c.name
            """, bind=sql.engine
        )
        rs = query.execute(election_id=election_id, question_id=question_id).fetchall()
    else:
        query = sql.text("""
            select c.candidate_id, c.ward, c.name
            from election_candidates c
            where c.candidate_id not in (
                select c.candidate_id
                from election_candidates c
                left join election_responses r
                on c.candidate_id = r.candidate_id
                where r.question_id = :question_id
                and c.election_id = :election_id
            )
            and c.withdrawn != 1
            and c.ward = :ward
            order by c.ward, c.name
            """, bind=sql.engine
        )
        rs = query.execute(election_id=election_id, question_id=question_id, ward=ward).fetchall()
    if len(rs) == 0:
        return []
    responses = []
    for row in rs:
        responses.append({
            'url': '%s/candidate/%s/%s' % (stub, row.candidate_id, election_id, ),
            'candidate_id': row.candidate_id,
            'ward': row.ward,
            'name': row.name,
        })
    return responses


def get_articles(election_id, doctype):
    """
    Returns a list of RTH articles related to the election
    """
    if doctype == 'article':
        query = sql.text("""
            select a.id as orig_id, a.title, a.date_issued, au.auth_name
            from elections e
            inner join articles a on e.section = a.section
            inner join authors au on a.auth_id = au.auth_id
            where e.election_id = :election_id
            order by a.id
            """, bind=sql.engine
        )
    elif doctype == 'blog':
        query = sql.text("""
            select a.blog_id as orig_id, a.title, a.date_issued, au.auth_name
            from elections e
            inner join blog a on e.section = a.section
            inner join authors au on a.auth_id = au.auth_id
            where e.election_id = :election_id
            order by a.blog_id
            """, bind=sql.engine
        )
    else:
        return []
    
    rs = query.execute(election_id=election_id).fetchall()
    documents = []
    for row in rs:
        documents.append({
            'url': 'http://raisethehammer.org/%s/%s' % (doctype, row.orig_id),
            'title': row.title,
            'author': row.auth_name,
            'date_issued': row.date_issued,
        })
    return documents


def get_apps(election_id):
    """
    Returns a list of known third-party apps built on the RTH Elections API.
    """
    apps = []
    query = sql.text("""
        select * 
        from election_apps 
        where election_id = :election_id
        """, bind=sql.engine
    )
    rs = query.execute(election_id=election_id).fetchall()
    for row in rs:
        apps.append({ 
            'title': row.title,
            'url': row.url,
        })
    return apps
            
