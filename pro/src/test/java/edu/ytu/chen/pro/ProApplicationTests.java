package edu.ytu.chen.pro;

import com.fasterxml.jackson.databind.ObjectMapper;
import edu.ytu.chen.pro.DAO.SolutionMapper;
import edu.ytu.chen.pro.commons.MapperUtils;
import edu.ytu.chen.pro.entity.IndexInfo;
import edu.ytu.chen.pro.entity.IndexJsonInfo;
import edu.ytu.chen.pro.service.HttpCrawlService;
import edu.ytu.chen.pro.service.PythonService;
import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.*;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = ProApplication.class)
public class ProApplicationTests {

    @Autowired
    private SolutionMapper solutionMapper;

    @Autowired
    private PythonService pythonService;

    @Autowired
    private HttpCrawlService httpCrawlService;

    @Test
    public void testMybatis(){
        List<IndexInfo> indexInfos = solutionMapper.getTotalIndexInfo();
        for (IndexInfo indexInfo : indexInfos) {
            System.out.println(indexInfo.getMd());
        }
    }

    @Test
    public void testCorrectIndexInfo(){
        List<IndexInfo> indexInfos = solutionMapper.getCorrectIndexInfo();
        for (IndexInfo indexInfo : indexInfos) {
            System.out.println(indexInfo.getC());
        }
    }

    @Test
    public void testJsonMapper(){
        List<IndexInfo> total = solutionMapper.getTotalIndexInfo();
        List<IndexInfo> correct = solutionMapper.getCorrectIndexInfo();
        List<IndexJsonInfo> infos = new ArrayList<>();
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd");
        for(int i = 0 ; i < total.size() && i < correct.size() ; i++){
            IndexJsonInfo info = new IndexJsonInfo();
            Date date = new Date(new Long(total.get(i).getMd()));
            info.setMd(df.format(date));
            info.setC1(Integer.parseInt(total.get(i).getC()));
            info.setC2(Integer.parseInt(correct.get(i).getC()));
            infos.add(info);
        }
        try {
            String text = MapperUtils.obj2json(infos);
            System.out.println(text);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    @Test
    public void getPythonInfo(){
        final String pythonInfo = pythonService.getPythonInfo();
        System.out.println(pythonInfo);
    }

    @Test
    public void formatJson(){
//        String s = "{\"0\":\"201758505132\",\"1\":\"201758505145\",\"2\":\"201758505125\",\"3\":\"201758505122\",\"4\":\"201758505116\",\"5\":\"201758505146\",\"6\":\"201758505107\",\"7\":\"201758505105\",\"8\":\"201758505124\",\"9\":\"201758505109\",\"10\":\"201758505141\",\"11\":\"201758505104\",\"12\":\"201758505138\",\"13\":\"201758505110\",\"14\":\"201758505140\",\"15\":\"201758505102\",\"16\":\"201758505147\",\"17\":\"201758505142\",\"18\":\"201758505106\",\"19\":\"201758505111\",\"20\":\"201758505119\",\"21\":\"201758505113\",\"22\":\"201758505118\",\"23\":\"201758505129\",\"24\":\"201758505120\",\"25\":\"201758505115\",\"26\":\"201758505152\",\"27\":\"201758505137\",\"28\":\"201758505103\",\"29\":\"201758505123\",\"30\":\"201758505148\",\"31\":\"201758505108\",\"32\":\"201758505149\",\"33\":\"201758505135\",\"34\":\"201758505139\",\"35\":\"201758505151\",\"36\":\"201758505114\",\"37\":\"201758505128\",\"38\":\"201758505130\",\"39\":\"201758505101\",\"40\":\"201758505126\",\"41\":\"201758505150\",\"42\":\"201758505131\",\"43\":\"201758505127\",\"44\":\"201758505136\",\"45\":\"201758505143\",\"46\":\"201758505144\",\"47\":\"201758505117\"}";
//        ObjectMapper mapper = new ObjectMapper();
//        try {
//            Map readValue = mapper.readValue(s,Map.class);
//            System.out.println(readValue);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
        final String pythonInfo = pythonService.getPythonInfo();
        String[] split = pythonInfo.split("\n");
        ObjectMapper mapper = new ObjectMapper();
        Map stuNum = null;
        Map pre = null;
        try {
            stuNum = mapper.readValue(split[0], Map.class);
            pre = mapper.readValue(split[1],Map.class);
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println(stuNum);
        System.out.println(pre.get("0"));
        /**
         * 输出：
         * {0=201758505132, 1=201758505145, 2=201758505125, 3=201758505122, 4=201758505116, 5=201758505146, 6=201758505107, 7=201758505105, 8=201758505124, 9=201758505109, 10=201758505141, 11=201758505104, 12=201758505138, 13=201758505110, 14=201758505140, 15=201758505102, 16=201758505147, 17=201758505142, 18=201758505106, 19=201758505111, 20=201758505119, 21=201758505113, 22=201758505118, 23=201758505129, 24=201758505120, 25=201758505115, 26=201758505152, 27=201758505137, 28=201758505103, 29=201758505123, 30=201758505148, 31=201758505108, 32=201758505149, 33=201758505135, 34=201758505139, 35=201758505151, 36=201758505114, 37=201758505128, 38=201758505130, 39=201758505101, 40=201758505126, 41=201758505150, 42=201758505131, 43=201758505127, 44=201758505136, 45=201758505143, 46=201758505144, 47=201758505117}
         * A
         */
    }

    @Test
    public void testHttpClient(){
        // 创建 HttpClient 客户端
        CloseableHttpClient httpClient = HttpClients.createDefault();

        // 创建 HttpGet 请求
        HttpGet httpGet = new HttpGet("http://202.194.119.110/ranklist.php?prefix=201758501101");
        // 设置长连接
        httpGet.setHeader("Connection", "keep-alive");
        // 设置代理（模拟浏览器版本）
        httpGet.setHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36");
        CloseableHttpResponse httpResponse = null;
        try {
            // 请求并获得响应结果
            httpResponse = httpClient.execute(httpGet);
            HttpEntity httpEntity = httpResponse.getEntity();
            // 输出请求结果
            Document doc = Jsoup.parse(EntityUtils.toString(httpEntity));
//            System.out.println(EntityUtils.toString(httpEntity));
            String text = doc.selectFirst("body > div.container > div > table > tbody > tr.evenrow > td:nth-child(4) > div").text();
            System.out.println(text);
        } catch (IOException e) {
            e.printStackTrace();
        }

        // 无论如何必须关闭连接
        finally {
            if (httpResponse != null) {
                try {
                    httpResponse.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            if (httpClient != null) {
                try {
                    httpClient.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    @Test
    public void testHttpCrawl(){
        final String pythonInfo = pythonService.getPythonInfo();
        String[] split = pythonInfo.split("\n");
        ObjectMapper mapper = new ObjectMapper();
        Map stuNum = null;
        Map pre = null;
        try {
            stuNum = mapper.readValue(split[0], Map.class);
            pre = mapper.readValue(split[1],Map.class);
        } catch (IOException e) {
            e.printStackTrace();
        }
        List<String> nickNames = httpCrawlService.getNickName(stuNum);
        for (String nickName : nickNames) {
            System.out.println(nickName);
        }
    }

    @Test
    public void testJsoup(){
        Connection connect = Jsoup.connect("http://202.194.119.110/ranklist.php?prefix=201758501101");
        connect.header("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36");
        Document doc = null;
        try {
            doc = connect.get();
        } catch (IOException e) {
            e.printStackTrace();
        }
        assert doc != null;
        String text = doc.selectFirst("body > div.container > div > table > tbody > tr.evenrow > td:nth-child(4) > div").text();
        System.out.println(text);
    }

    @Test
    public void testSubmitData(){
        List<IndexInfo> totalData = solutionMapper.getTotalData("201758501101");
        SimpleDateFormat df = new SimpleDateFormat("MMM",Locale.ENGLISH);
        for (IndexInfo totalDatum : totalData) {
            System.out.println(totalDatum.getMd()+"|"+totalDatum.getC());
        }
        System.out.print("[");
        String tmp = "";
        for(int i = 0 ; i < totalData.size() ; i++){
            Date date = new Date(new Long(totalData.get(i).getMd()));
            if(!tmp.equals(df.format(date)))
                System.out.print("'"+df.format(date)+"',");
            else
                System.out.print("'',");
            tmp = df.format(date);
        }
        System.out.println("]");
        System.out.print("[");
        for(int i = 0 ; i < totalData.size() ; i++){
            System.out.print(totalData.get(i).getC()+",");
        }
        System.out.println("]");
        System.out.print("[");
        List<IndexInfo> acceptData = solutionMapper.getAcceptData("201758501101");
        for (IndexInfo acceptDatum : acceptData) {
            System.out.print(acceptDatum.getC()+",");
        }
        System.out.println("]");
    }

    @Test
    public void testPIEData(){
        String stuNum = "201758501101";
        List<Integer> pieData = solutionMapper.getPieData(stuNum);
        for (Integer pieDatum : pieData) {
            System.out.println(pieDatum);
        }
    }

}
