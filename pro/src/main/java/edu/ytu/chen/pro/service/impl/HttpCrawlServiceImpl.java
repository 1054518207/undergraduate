package edu.ytu.chen.pro.service.impl;

import edu.ytu.chen.pro.service.HttpCrawlService;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

@Service
public class HttpCrawlServiceImpl implements HttpCrawlService {

    private static final String BASEURI = "http://202.194.119.110/ranklist.php?prefix=";

    @Override
    public List<String> getNickName(Map<String,String> map) {
        List<String> list = new LinkedList<>();
        for(int i = 0 ; i < map.size() ; i++){
            String stuNum = map.get(String.valueOf(i));
            if(stuNum != null)
                list.add(stuNum);
        }
        return getNickByStuNum(list);
    }

    private List<String> getNickByStuNum(List<String> stuNumList) {
        List<String> nickNames = new LinkedList<>();
        for (String stuNum : stuNumList) {
            Connection connect = Jsoup.connect(BASEURI+stuNum);
            connect.header("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36");
            Document doc = null;
            try {
                doc = connect.get();
            } catch (IOException e) {
                e.printStackTrace();
            }
            assert doc != null;
            String text = doc.selectFirst("body > div.container > div > table > tbody > tr.evenrow > td:nth-child(4) > div").text();
            nickNames.add(text);
        }
        return nickNames;
    }
}
