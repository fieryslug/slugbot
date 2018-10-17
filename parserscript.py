import json
import utils

def main():
    
    #crawlysave(utils.aqua_slug, 'cn.json')
    #crawlysave(utils.flamma_slug, 'hn.json')
    #crawlysave(utils.terra_slug, 'c8.json')
    #crawlysave(utils.aer_slug, 'h8.json')
    #crawlysave(utils.lux_slug, 'hhchs.json')
    #crawlysave(utils.test_slug, 'test.json')
    crawlysave(utils.ignis_slug, 'ohn.json')

def crawlysave(slug, dest):
    r = slug.crawl()
    print(r)
    posts = []
    saves = []

    cnt = 0
    while True:

        if 'data' in r:
            posts = r['data']

        for post in posts:
            if 'message' in post:
                msg = str(post['message'])
                saves.append(msg)
                print(msg)
                cnt += 1
                print('---------{}---------'.format(cnt))

        if 'paging' in r:
            if 'next' in r['paging']:
                r = slug.crawl(r['paging']['next'])
            else:
                break
        else:
            break

    with open('source/parsed/' + dest, 'w+') as f:
        json.dump(saves, f)




def crawlC():

    r = utils.aqua_slug.crawl()
    posts = []
    saves = []

    cnt = 0
    while True:

        if 'data' in r:
            posts = r['data']

        for post in posts:
            if 'message' in post:
                msg = str(post['message'])
                saves.append(msg)
                print(msg)
                cnt += 1
                print('---------{}---------'.format(cnt))

        if 'paging' in r:
            if 'next' in r['paging']:
                r = utils.aqua_slug.crawl(r['paging']['next'])
            else:
                break
        else:
            break

    return saves




if __name__ == '__main__':
    main()
