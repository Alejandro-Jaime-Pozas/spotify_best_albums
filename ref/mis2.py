import requests, re, json, difflib


# CHECK SIMILARITY BW ACCLAIMED VS SPOTIFY RESULTS
def similarity_score(accl_artist, 
                     accl_album, 
                     spot_artist_name, 
                     spot_album_name,
                     accl_year, 
                     spot_album_year):
    # Convert the strings to lowercase to make the comparison case-insensitive
    accl_artist, accl_album = accl_artist.lower(), accl_album.lower()
    spot_artist_name, spot_album_name = spot_artist_name.lower(), spot_album_name.lower()
    # Remove everythiinng in parentheses or [] from all spotify album names
    spot_album_name_clean = re.sub(r'\([^)]*\)', '', re.sub(r'\[[^\]]*\]', '', spot_album_name))
    # Calculate the similarity ratio between the two strings
    artist_similarity_ratio = difflib.SequenceMatcher(None, accl_artist, spot_artist_name).quick_ratio()
    album_similarity_ratio = difflib.SequenceMatcher(None, accl_album, spot_album_name_clean).quick_ratio()
    accl_artist_album = f'''{accl_artist} {accl_album}'''
    spot_artist_album = f'''{spot_artist_name} {spot_album_name_clean}'''
    overall_similarity_ratio = difflib.SequenceMatcher(None, accl_artist_album, spot_artist_album).quick_ratio()

    # CREATE A SCORE SYSTEM UP TO 5, SO THAT THE HIGHEST MATCHING ALBUM GOES THROUGH
    # First filter: if overall > 0.90, then album is a match (manually checked this)
    if overall_similarity_ratio > 0.90:
        overall_similarity_ratio += 9
    else:
        overall_similarity_ratio += artist_similarity_ratio + album_similarity_ratio
        # 2nd filter: if accl_artist name split at spaces is not in at least 1 of spot_artist name split, reject
        # print(accl_artist.split(' '))
        # print(spot_artist_name.split(' '))
        accl_artist_list = accl_artist.split()
        match_artist_words = 0
        for word in accl_artist_list:
            if word.isalnum() and word not in ('the', 'and', 'with', 'of', 'at', 'to', 'in'):
                    if word in spot_artist_name.split():
                        # print(f'{word}: is the word that matches')
                        match_artist_words += 1
                        overall_similarity_ratio += 0.5
        if match_artist_words == 0:
            overall_similarity_ratio = 0
        # 3rd filter: if less than 50% of the 'main' words from album names match, reject
        exclude_from_album = accl_artist_list + ['the', 'of', 'to', 'and', 'at', 'with', 'is', 'in']
        # print(f'words NOT to match album: {exclude_from_album}')
        # print(f'acclaimed album: {accl_album}')
        # try:
        #     print(f'spotify album: {spot_album_name_clean} - ratio: {album_similarity_ratio}')
        # except:
        #     print('spotify album NOT FOUND')
        accl_album_words = [word for word in accl_album.split() if word not in exclude_from_album]
        accl_album_words_list = []
        for word in accl_album_words:
            cleaned_word = re.sub(r'[^a-zA-Z0-9]', '', word)
            if cleaned_word:
                accl_album_words_list.append(cleaned_word)
        # if final album list length > 0, check if < 50% of length is in spot_album_name, reject
        # print(f'WORDS MATCHED: {accl_album_words_list}', '\n')
        if len(accl_album_words_list) > 0:
            # NEED TO INCREASE SCORE FOR ALBUMS THAT HAVE MORE WORDS THAT MATCH ORIGINAL ALBUM
            match_album_words = 0
            for word in accl_album_words_list:
                if word in spot_album_name_clean:
                    match_album_words += 1
                    overall_similarity_ratio += 0.1
            if match_album_words == 0: #/ len(accl_album_words_list) < 0.5:
                overall_similarity_ratio = 0
        # remove points for deluxe/expanded albums
        if 'expanded' in spot_album_name or 'deluxe' in spot_album_name:
            overall_similarity_ratio -= 0.04
        # if accl_year == spot_album_year: # this could benefit similar ratio albums that actually dont match
        #     overall_similarity_ratio += 0.10 
        else:
            # if album only has the artist's name in album, check if name matches, else reject
            # print(accl_artist_list)
            album_only_has_artist_name = 0
            for word in accl_artist_list:
                if word.isalnum() and word not in ('the', 'and', 'with', 'of', 'at', 'to', 'in', 'is'):
                    if word in spot_album_name_clean:
                        album_only_has_artist_name += 1
            if album_only_has_artist_name == 0:
                overall_similarity_ratio = 0


    return {    
            "overall_similarity_ratio": overall_similarity_ratio, 
            "artist_similarity_ratio": artist_similarity_ratio, 
            "album_similarity_ratio": album_similarity_ratio
        }

print(similarity_score())


# FOR EACH ALBUM RESULT, COLLECT ITS SIMILARITY TO ACCLAIMED MUSIC ALBUM, RETURN THE HIGHEST RESULT MATCH
# NEED TO CHANGE THIS TO CREATE HIGHER QUALITY MATCHES FOR ARTIST/ALBUMS
def get_album_match(spotify_results_list, accl_artist, accl_album, accl_year, list_data):

    top_album_overall_score = 0
    top_album_artist_score = 0
    top_album_score = 0
    top_album_id = None 
    top_album_artist_name = None 
    top_album_name = None 
    top_match_artist_words = 0 
    top_match_album_words = 0 

    for result in spotify_results_list:
        spot_album_id = result['id']
        spot_artist_name = result['artists'][0]['name'] # may need to change encoding here
        spot_album_name = result['name'] # may need to change encoding here
        spot_album_year = int(result['release_date'][:4])
        # print(spot_album_id)

        similarity = similarity_score(accl_artist, 
                                      accl_album, 
                                      spot_artist_name, 
                                      spot_album_name,
                                      accl_year, 
                                      spot_album_year)
        # # PRINT RESULTS FROM BOTH SITES, ALONG W/SIMILARITY
        # print(f'''REAL ARTIST: {accl_artist}
        #       === REAL ALBUM: {accl_album} - YEAR: {accl_year}''')
        # try:
        #     print(f'''SPOTIFY ARTIST: {spot_artist_name}
        #           === SPOTIFY ALBUM: {spot_album_name} - YEAR: {spot_album_year}''')
        # except UnicodeEncodeError as e:
        #     print('Unable to print due to Unicode Error!!!')
        # print(f'''SIMILARITY: {similarity[0]:.2f}''')
        # print()

        # fheck if score, artist, album matches are > previous iterations
        if similarity["overall_similarity_ratio"] > top_album_overall_score:
            # if similarity["match_album_words"] >= top_match_album_words:
            top_album_id = spot_album_id
            top_album_artist_name = spot_artist_name
            top_album_name = spot_album_name
            top_album_overall_score = similarity["overall_similarity_ratio"]
            top_album_artist_score = similarity["artist_similarity_ratio"]
            top_album_score = similarity["album_similarity_ratio"]

        # elif similarity["match_artist_words"] >= top_match_artist_words:
        #     if similarity["match_album_words"] > top_match_album_words:
        #         top_album_id = spot_album_id
        #         top_album_artist_name = spot_artist_name
        #         top_album_name = spot_album_name
        #         top_album_overall_score = similarity["overall_similarity_ratio"]
        #         top_album_artist_score = similarity["artist_similarity_ratio"]
        #         top_album_score = similarity["album_similarity_ratio"]

        # elif similarity["match_album_words"] >= top_match_album_words:
        #     if similarity["match_artist_words"] > top_match_artist_words:
        #         top_album_id = spot_album_id
        #         top_album_artist_name = spot_artist_name
        #         top_album_name = spot_album_name
        #         top_album_overall_score = similarity["overall_similarity_ratio"]
        #         top_album_artist_score = similarity["artist_similarity_ratio"]
        #         top_album_score = similarity["album_similarity_ratio"]



    # add an upper limit to reject albums below that limit
    limit = 0.35

    # ADD THE ALBUM DATA TO A DICTIONARY
    data = {
        'spot_top_album_id': top_album_id, 
        'spot_top_album_artist_name': top_album_artist_name, 
        'accl_album_artist_name': accl_artist, 
        'top_album_artist_score': top_album_artist_score, 
        'spot_top_album_name': top_album_name, 
        'accl_album_name': accl_album, 
        'top_album_score': top_album_score, 
        'top_album_overall_score': top_album_overall_score, 
        'year': accl_year,
        'album_found': True if top_album_overall_score > limit else False, 
        }
    list_data.append(data)

    # TODO - IF SIMILARTY SCORE IS BELOW X AMOUNT, DON'T ADD THE ALBUM
    if top_album_overall_score < limit or top_album_id == None:
        print(f'''THERE IS NO !!!!!!!!!!!!!! MATCH FOR THIS ALBUM: {accl_artist} {accl_album}''')
        return None 
    
    print(f'''ADDED TO SPOTIFY: {top_album_artist_name} - {top_album_name}\n''')
    return data 