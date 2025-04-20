import xml.etree.ElementTree as ET
import psycopg2
from psycopg2 import sql

set_user = "postgres"
set_password = "1579"
path_to_xml_files_folder = "data\\dba.stackexchange.com\\"

def connect():
    return psycopg2.connect(
        dbname = "StackExchange",
        user = set_user,
        password = set_password,
        host="localhost"
    )

def get_rows(xml_file_name):
    path_to_xml = path_to_xml_files_folder + xml_file_name + ".xml"
    tree = ET.parse(path_to_xml)
    root = tree.getroot()
    replace_apostrophes(root)

    return root.findall('row')


def replace_apostrophes(element):
    if element.text and "'" in element.text:
        element.text = element.text.replace("'", "&apos;")
    
    for attr in element.attrib:
        if "'" in element.attrib[attr]:
            element.attrib[attr] = element.attrib[attr].replace("'", "&apos;")
    
    for child in element:
        replace_apostrophes(child)


def inserting_users(cur):
    users = get_rows("Users")
    all_user_ids = set()

    for user in users:
        id = user.get('Id')
        reputation = user.get('Reputation')
        creation_date = user.get('CreationDate')
        display_name = user.get('DisplayName')
        last_access_date = user.get('LastAccessDate')
        website_url = user.get('WebsiteUrl')
        location = user.get('Location')
        about_me = user.get('AboutMe')
        views = user.get('Views')
        up_votes = user.get('UpVotes')
        down_votes = user.get('DownVotes')
        account_id = user.get('AccountId')
        
        cur.execute("""
            INSERT INTO "users" (id, reputation, creation_date, display_name, last_access_date, website_url, location, about_me, views, up_votes, down_votes, account_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id, reputation, creation_date, display_name, last_access_date, website_url, location, about_me, views, up_votes, down_votes, account_id))
        
        all_user_ids.add(id)

    return all_user_ids



def inserting_badges(cur, user_ids):
    badges = get_rows("Badges")

    for badge in badges:
        id = badge.get('Id')
        user_id = badge.get('UserId')
        name = badge.get('Name')
        date = badge.get('Date')
        tag_class = badge.get('Class')
        tag_based = badge.get('TagBased')

        if (user_id in user_ids):
            cur.execute("""
                INSERT INTO "badges" (id, user_id, name, date, class, tag_based)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id, user_id, name, date, tag_class, tag_based))



def inserting_post_types(cur):
    file = open("data\\PostTypes.txt", "r")
    all_post_type_ids = set()

    for line in file:
        split_index = line.find('=')
        id = line[0 : split_index - 1]
        name = line[split_index + 2 : len(line) - 1]
        
        cur.execute("""
            INSERT INTO "post_types" (id, name)
            VALUES (%s, %s)
        """, (id, name))

        all_post_type_ids.add(id)

    return all_post_type_ids



def inserting_posts(cur, post_type_ids, user_ids):
    posts = get_rows("Posts")
    all_post_ids = set()

    for post in posts:
        id = post.get('Id')
        post_type_id = post.get('PostTypeId')
        creation_date = post.get('CreationDate')
        score = post.get('Score')
        view_count = post.get('ViewCount')
        body = post.get('Body')
        owner_user_id = post.get('OwnerUserId')
        owner_display_name = post.get('OwnerDisplayName')
        last_editor_user_id = post.get('LastEditorUserId')
        last_editor_display_name = post.get('LastEditorDisplayName')
        last_edit_date = post.get('LastEditDate')
        last_activity_date = post.get('LastActivityDate')
        title = post.get('Title')
        tags = post.get('Tags')
        answer_count = post.get('AnswerCount')
        comment_count = post.get('CommentCount')
        favorite_count = post.get('FavoriteCount')
        closed_date = post.get('ClosedDate')
        community_owned_date = post.get('CommunityOwnedDate')

        if ((owner_user_id in user_ids) and (post_type_id in post_type_ids)):
            cur.execute("""
                INSERT INTO "posts" (id, post_type_id, accepted_answer_id, parent_id, creation_date, score, view_count, body, owner_user_id, owner_display_name, last_editor_user_id, last_editor_display_name, last_edit_date, last_activity_date, title, tags, answer_count, comment_count, favorite_count, closed_date, community_owned_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (id, post_type_id, None, None, creation_date, score, view_count, body, owner_user_id, owner_display_name, last_editor_user_id, last_editor_display_name, last_edit_date, last_activity_date, title, tags, answer_count, comment_count, favorite_count, closed_date, community_owned_date))
        
            all_post_ids.add(id)

    for post in posts:
        id = post.get('Id')
        accepted_answer_id = post.get('AcceptedAnswerId')
        parent_id = post.get('ParentId')

        if (accepted_answer_id in all_post_ids):
            cur.execute("""
                UPDATE "posts" 
                SET accepted_answer_id = %s
                WHERE id = %s
            """, (accepted_answer_id, id))
            
        if (parent_id in all_post_ids):
            cur.execute("""
                UPDATE "posts" 
                SET parent_id = %s
                WHERE id = %s
        """, (parent_id, id))

    return all_post_ids



def inserting_link_types(cur):
    file = open("data\\LinkTypes.txt", "r")
    all_link_type_ids = set()

    for line in file:
        line_parts = line.split()
        id = line_parts[0]
        name = line_parts[2]

        cur.execute("""
            INSERT INTO "link_types" (id, name)
            VALUES (%s, %s)
        """, (id, name))

        all_link_type_ids.add(id)

    return all_link_type_ids



def inserting_post_links(cur, post_ids, link_type_ids):
    post_links = get_rows("PostLinks")

    for post_link in post_links:
        id = post_link.get('Id')
        creation_date = post_link.get('CreationDate')
        post_id = post_link.get('PostId')
        related_post_id = post_link.get('RelatedPostId')
        link_type_id = post_link.get('LinkTypeId')

        if ((post_id in post_ids) and (related_post_id in post_ids) and (link_type_id in link_type_ids)):
            cur.execute("""
                INSERT INTO "post_links" (id, creation_date, post_id, related_post_id, link_type_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (id, creation_date, post_id, related_post_id, link_type_id))



def inserting_comments(cur, user_ids, post_ids):
    comments = get_rows("Comments")

    for comment in comments:
        id = comment.get('Id')
        post_id = comment.get('PostId')
        score = comment.get('Score')
        text_field = comment.get('TextField')
        creation_date = comment.get('CreationDate')
        user_display_name = comment.get('UserDisplayName')
        user_id = comment.get('UserId')

        if ((post_id in post_ids) and (user_id in user_ids)):
            cur.execute("""
                INSERT INTO "comments" (id, post_id, score, text_field, creation_date, user_display_name, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (id, post_id, score, text_field, creation_date, user_display_name, user_id))



def inserting_tags(cur, post_ids):
    tags = get_rows('Tags')

    for tag in tags:
        id = tag.get('Id')
        tag_name = tag.get('TagName')
        count = tag.get('Count')
        excpert_post_id = tag.get('ExcerptPostId')
        wiki_post_id = tag.get('WikiPostId')

        if ((excpert_post_id in post_ids) and (wiki_post_id in post_ids)):
            cur.execute("""
                INSERT INTO "tags" (id, tag_name, count, excpert_post_id, wiki_post_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (id, tag_name, count, excpert_post_id, wiki_post_id))
                


def inserting_vote_types(cur):
    file = open("data\\VoteTypes.txt", "r")
    all_vote_type_ids = set()

    for line in file:
        line_parts = line.split()
        id = line_parts[0]
        name = line_parts[2]

        cur.execute("""
            INSERT INTO "vote_types" (id, name)
            VALUES (%s, %s)
        """, (id, name))

        all_vote_type_ids.add(id)

    return all_vote_type_ids



def inserting_votes(cur, post_ids, vote_type_ids):
    votes = get_rows('Tags')

    for vote in votes:
        id = vote.get('Id')
        post_id = vote.get('PostId')
        vote_type_id = vote.get('VoteTypeId')
        creation_date = vote.get('CreationDate')

        if ((post_id in post_ids) and (vote_type_id in vote_type_ids)):
            cur.execute("""
                INSERT INTO "votes" (id, post_id, vote_type_id, creation_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (id, post_id, vote_type_id, creation_date))



def inserting_post_history_types(cur):
    file = open("data\\PostHistoryTypes.txt", "r")
    all_post_history_type_ids = set()

    for line in file:
        split_index_1 = line.find('=')
        id = line[0 : split_index_1 - 1]

        split_index_2 = line.find('-')
        if (split_index_2 != -1):
            name = line[split_index_1 + 2 : len(line)]
        else:
            name = line[split_index_1 + 2 : split_index_2 - 1]

        if ((id != "") and (name != "")):
            cur.execute("""
                INSERT INTO "post_history_types" (id, name)
                VALUES (%s, %s)
            """, (id, name))

            all_post_history_type_ids.add(id)

    return all_post_history_type_ids



def inserting_post_history(cur, post_history_type_ids, post_ids, user_ids):
    post_histories = get_rows('PostHistory')

    for post_history in post_histories:
        id = post_history.get('Id')
        post_history_type_id = post_history.get('PostHistoryTypeId')
        post_id = post_history.get('PostId')
        revision_guid = post_history.get('RevisionGUID')
        creation_date = post_history.get('CreationDate')
        user_id = post_history.get('UserId')
        user_display_name = post_history.get('UserDisplayName')
        comment = post_history.get('Comment')
        text = post_history.get('Text')

        if ((post_history_type_id in post_history_type_ids) and (post_id in post_ids) and (user_id in user_ids)):
            cur.execute("""
                INSERT INTO "post_history" (id, post_history_type_id, post_id, revision_guid, creation_date, user_id, user_display_name, comment, text)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (id, post_history_type_id, post_id, revision_guid, creation_date, user_id, user_display_name, comment, text))


    


def main():
    try:
        conn = connect()
        conn.autocommit = False
        cur = conn.cursor()

        print("Inserting started...")

        user_ids = inserting_users(cur)
        print("Users inserted")

        inserting_badges(cur, user_ids)
        print("Badges inserted")

        post_type_ids = inserting_post_types(cur)
        print("PostTypes inserted")

        post_ids = inserting_posts(cur, post_type_ids, user_ids)
        print("Posts inserted")
        
        link_type_ids = inserting_link_types(cur)
        print("LinkTypes inserted")

        inserting_post_links(cur, post_ids, link_type_ids)
        print("PostLinks inserted")

        inserting_comments(cur, user_ids, post_ids)
        print("Comments inserted")

        inserting_tags(cur, post_ids)
        print("Tags inserted")

        vote_type_ids = inserting_vote_types(cur)
        print("VoteTypes inserted")
       
        inserting_votes(cur, post_ids, vote_type_ids)
        print("Votes inserted")

        post_history_type_ids = inserting_post_history_types(cur)
        print("PostHistoryTypes inserted")

        inserting_post_history(cur, post_history_type_ids, post_ids, user_ids)
        print("PostHistory inserted")

        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()


