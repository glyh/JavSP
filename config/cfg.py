#type: ignore

from javspn.core.config import CfgObj


# 推测番号前忽略文件名中的特定字符串数组(忽略大小写)
# 大多数情况软件能够自动识别番号，只有当文件名中特定的部分导致番号识别错误时才需要更新此设置
MovieID = CfgObj()
# 要忽略的字串（全词匹配）
MovieID.ignore_whole_word = ['144P', '240P', '360P', '480P', '720P', '1080P', '2K', '4K']
# 要忽略的正则表达式（如果你不熟悉正则表达式，请不要修改此配置，否则可能严重影响番号识别效果）
MovieID.ignore_regex = r'\w+2048\.com;Carib(beancom)?;[^a-z\d](f?hd|lt)[^a-z\d]'

File = CfgObj()
# 整理哪个文件夹下的影片？（此项留空时将在运行时询问）
File.scan_dir = None
## 哪些后缀的文件应当视为影片？
File.media_ext = ["3gp", "avi", "f4v", "flv", "iso", "m2ts", "m4v", "mkv", "mov", "mp4", "mpeg", "rm", "rmvb", "ts", "vob", "webm", "wmv", "strm", "mpg"]
# 扫描影片文件时忽略指定的文件夹（以.开头的文件夹不需要设置也会被忽略）
File.ignore_folder = ["#recycle", "#整理完成", "不要扫描"]
# 匹配番号时忽略小于指定大小的文件（以MiB为单位，0表示禁用此功能）
File.ignore_video_file_less_than = 232
# 整理时是否移动文件: True-移动所有文件到新文件夹; False-数据保存到同级文件夹，不移动文件
File.enable_file_move = True

Network = CfgObj()
# 是否启用代理
Network.use_proxy = False
# 设置代理服务器地址，支持 http, socks5/socks5h 代理。示例格式如下：
Network.proxy = 'http://127.0.0.1:20171'
# 网络问题导致抓取数据失败时的重试次数，通常3次就差不多了
Network.retry = 3
Network.timeout = 10

# 要使用的爬虫列表（汇总数据时从前到后进行）
# airav avsox avwiki fanza fc2 fc2fan javbus javdb javlib javmenu jav321 msin mgstage prestige
CrawlerSelect = CfgObj()
CrawlerSelect.normal = ['airav', 'avsox', 'javbus', 'javdb', 'javlib', 'jav321', 'mgstage', 'prestige']
CrawlerSelect.fc2 = ['fc2', 'msin', 'avsox', 'javdb', 'javmenu']
CrawlerSelect.cid = ['fanza']
CrawlerSelect.getchu = ['dl_getchu']
CrawlerSelect.gyutto = ['gyutto']

Crawler = CfgObj()
# 爬虫至少要获取到哪些字段才可以视为抓取成功？
Crawler.required_keys = ['cover', 'title']
# 努力爬取更准确更丰富的信息（会略微增加部分站点的爬取耗时）
Crawler.hardworking_mode = True
# 使用网页番号作为最终番号（启用时会对番号大小写等进行更正）
Crawler.respect_site_avid = True
# fc2fan已关站。如果你有镜像，请设置本地镜像文件夹的路径，此文件夹内要有类似'FC2-12345.html'的网页文件
Crawler.fc2fan_local_path = None
# 标题处理：删除尾部可能存在的女优名
Crawler.title__remove_actor = True
# 标题处理：优先使用中文标题（如果能获取到的话）
Crawler.title__chinese_first = True
# 刮削一部电影后的等待时间（秒，设置为0禁用此功能）
Crawler.sleep_after_scraping = 1
# 禁用javdb的封面（auto/yes/no, 默认auto: 如果能从别的站点获得封面则不用javdb的以避免水印）
Crawler.ignore_javdb_cover = 'auto'

# 各个站点的免代理地址。地址失效时软件会自动尝试获取新地址，你也可以手动设置
ProxyFree = CfgObj()
ProxyFree.avsox = 'https://avsox.click'
ProxyFree.javdb = 'https://javdb365.com'
ProxyFree.javbus = 'https://www.busdmm.shop'
ProxyFree.javlib = 'https://www.i71t.com'

# 配置整理时的命名规则
# save_dir, nfo_title和filename中可以使用变量来引用影片的数据，支持的变量列表见下面的地址:
# https://github.com/Yuukiy/JavSP/wiki/NamingRule-%7C-%E5%91%BD%E5%90%8D%E8%A7%84%E5%88%99
NamingRule = CfgObj()
# 设置媒体服务器类型 (universal/plex/emby/jellyfin/kodi/video_station, 默认universal: 按兼容性最高的方式命名封面和nfo)
NamingRule.media_servers = 'universal'
# 整理后的影片和封面等文件的保存位置
NamingRule.output_folder = '#整理完成'
# 存放影片、封面等文件的文件夹路径
NamingRule.save_dir = '{actress}/[{num}] {title}'
# 影片、封面、nfo信息文件等的文件名将基于下面的规则来创建
NamingRule.filename = '{num}'
# 允许的最长文件路径（路径过长时将据此自动截短标题）
NamingRule.max_path_len = 250
# 是否以字节数来计算文件路径长度（auto/yes/no, auto将自动根据输出路径的文件系统是本地还是远程来判断）
NamingRule.calc_path_len_by_byte = 'auto'
# 路径中的$actress字段最多包含多少名女优？
NamingRule.max_actress_count = 10
# nfo文件中的影片标题（即媒体管理工具中显示的标题）
NamingRule.nfo_title = '{num} {title}'
# 下面三个选项依次设置 已知有码/已知无码/不确定 这三种情况下 $censor 对应的文本(可以利用此变量将有码/无码影片整理到不同文件夹)
NamingRule.text_for_censored = '有码'
NamingRule.text_for_uncensored = '无码'
NamingRule.text_for_unknown_censorship = '打码情况未知'
# 下面这些项用来设置对应变量为空时的替代信息
NamingRule.null_for_title = '#未知标题'
NamingRule.null_for_actress = '#未知女优'
NamingRule.null_for_serial = '#未知系列'
NamingRule.null_for_director = '#未知导演'
NamingRule.null_for_producer = '#未知制作商'
NamingRule.null_for_publisher = '#未知发行商'

Picture = CfgObj()
# 尽可能下载高清封面？（高清封面大小约 8-10 MiB，远大于普通封面，如果你的网络条件不佳，会降低整理速度）
Picture.use_big_cover = True
# 是否下载剧照？
Picture.use_extra_fanarts = False
# 间隔的两次封面爬取请求之间应该间隔多久，单位为秒
Picture.extra_fanarts_scrap_interval = 2
# 启用图像识别裁剪海报
Picture.use_ai_crop = False
# 要使用图像识别来裁剪的番号系列($label), \d表示纯数字番号（FC2和识别到的无码影片会自动使用图像识别裁剪）
Picture.use_ai_crop_labels = ['\d', 'ARA', 'SIRO', 'GANA', 'MIUM']
# 要使用的图像识别引擎，详细配置见文档 https://github.com/Yuukiy/JavSP/wiki/AI-%7C-%E4%BA%BA%E8%84%B8%E8%AF%86%E5%88%AB
# 取值'pphumanseg', 'yunet' 或者 'baidu' 
Picture.ai_engine = None
# 百度人体分析应用的AppID（仅在图像识别引擎为baidu时需要）
Picture.aip_appid = None
# 百度人体分析应用的API Key（仅在图像识别引擎为baidu时需要）
Picture.aip_api_key = None 
# 百度人体分析应用的Secret Key（仅在图像识别引擎为baidu时需要）
Picture.aip_secret_key = None
# 在封面图上添加水印（标签），例如“字幕”
Picture.add_label_to_cover = False
# 如果使用yunet, 需要设置yunet模型位置，绝对或者相对。
# 请从下述链接中下载任意一个`.onnx`模型，放到和yunet_model对应的路径上
# https://github.com/opencv/opencv_zoo/tree/ec5b2c8af6b3505b28b7721f7d18528ac22afa2b/models/face_detection_yunet
Picture.yunet_model = None
# 如果使用pphumanseg, 需要设置pphumanseg模型位置，绝对或者相对。
# 请从下述链接中下载任意一个`.onnx`模型，放到和pphumanseg_model对应的路径上
# https://github.com/opencv/opencv_zoo/tree/ec5b2c8af6b3505b28b7721f7d18528ac22afa2b/models/human_segmentation_pphumanseg
Picture.pphumanseg_model = None

Translate = CfgObj()
# 翻译引擎，可选: google, bing, baidu （Google可以直接免费使用。留空表示禁用翻译功能）
# 进阶功能的文档 https://github.com/Yuukiy/JavSP/wiki/Translation-%7C-%E7%BF%BB%E8%AF%91
Translate.engine = None
# 是否翻译标题
Translate.translate_title = True
# 是否翻译剧情简介
Translate.translate_plot = True
# 百度翻译的APP ID和密钥
Translate.baidu_appid = None
Translate.baidu_key = None
# 微软必应翻译（Azure 认知服务 → 翻译）的密钥
Translate.bing_key = None

NFO = CfgObj()
# 同时将genre写入到tag？
NFO.add_genre_to_tag = True
# 是否开启艺名固定。如果允许，对于存在多个艺名的女优，会固定使用一个艺名
NFO.fix_actress_name = True

Other = CfgObj()
# 是否允许检查更新。如果允许，在有新版本时会显示提示信息和新版功能
Other.check_update = True
# 是否在刮削结束后自动退出软件
Other.auto_exit = False
# 是否在刮削结束后关机
Other.shutdown = False
# 不允许更新
Other.no_update = False
# 仅刮削data-cache-file缓存文件中的数据
Other.only_fetch = False
# 仅识别，不刮削
Other.only_scan = False
# 手动模式:让用户处理无法识别番号的影片（'all', 'failed'或者False）
Other.manual = False
# 存储数据的缓存文件，临时文件，供进程间通信使用
Other.data_cache_file = ''
