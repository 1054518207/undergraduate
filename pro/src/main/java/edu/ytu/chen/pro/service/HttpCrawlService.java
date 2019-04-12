package edu.ytu.chen.pro.service;

import java.util.List;
import java.util.Map;

public interface HttpCrawlService {

    /**
     * 根据map对应学号获取学号昵称
     * @param map 装有学号的map
     * @return 昵称列表
     */
    List<String> getNickName(Map<String,String> map);
}
