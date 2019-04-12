package edu.ytu.chen.pro.api;

import com.fasterxml.jackson.databind.ObjectMapper;
import edu.ytu.chen.pro.DAO.SolutionMapper;
import edu.ytu.chen.pro.commons.Constants;
import edu.ytu.chen.pro.commons.MapperUtils;
import edu.ytu.chen.pro.entity.IndexInfo;
import edu.ytu.chen.pro.entity.PersonInfoPie;
import edu.ytu.chen.pro.entity.PredictInfo;
import edu.ytu.chen.pro.service.HttpCrawlService;
import edu.ytu.chen.pro.service.PythonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.*;

@RestController
@RequestMapping(value = "api", method = RequestMethod.GET)
public class AjaxData {

    @Autowired
    private HttpCrawlService httpCrawlService;

    @Autowired
    private PythonService pythonService;

    @Autowired
    private SolutionMapper solutionMapper;

    private static final String BASEURI = "http://202.194.119.110/ranklist.php?prefix=";

    @RequestMapping(value = "names", method = RequestMethod.GET)
    public String getNameData(){
        final String pythonInfo = pythonService.getPythonInfo();
        String[] split = pythonInfo.split("\n");
        ObjectMapper mapper = new ObjectMapper();
        Map stuNum = null;
        Map predictLabel = null;
        try {
            stuNum = mapper.readValue(split[0], Map.class);
            predictLabel = mapper.readValue(split[1],Map.class);
        } catch (IOException e) {
            e.printStackTrace();
        }

        List<PredictInfo> levelA = new LinkedList<>();
        List<PredictInfo> levelD = new LinkedList<>();
        List<String> nickNames = httpCrawlService.getNickName(stuNum);

        for(int i = 0 ; i < predictLabel.size() ; i++)
            if("A".equals(predictLabel.get(String.valueOf(i)))){
                PredictInfo predictInfo =new PredictInfo();
                predictInfo.setLabel(nickNames.get(i));
                predictInfo.setUrl(BASEURI+stuNum.get(String.valueOf(i)));
                levelA.add(predictInfo);
            }else if("D".equals(predictLabel.get(String.valueOf(i)))){
                PredictInfo predictInfo =new PredictInfo();
                predictInfo.setLabel(nickNames.get(i));
                predictInfo.setUrl(BASEURI+stuNum.get(String.valueOf(i)));
                levelD.add(predictInfo);
            }

        String s = null;
        try {
            s = MapperUtils.obj2json(levelA);
            s += '|' + MapperUtils.obj2json(levelD);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return s;
    }

    @RequestMapping(value = "labels", method = RequestMethod.GET)
    public String getLabels(String stuNum){
        List<IndexInfo> totalData = solutionMapper.getTotalData(stuNum);
        SimpleDateFormat df = new SimpleDateFormat("MMM", Locale.ENGLISH);
        StringBuilder data = new StringBuilder("[");
        String tmp = "";
        for (IndexInfo totalDatum : totalData) {
            Date date = new Date(new Long(totalDatum.getMd()));
            if (!tmp.equals(df.format(date)))
                data.append("'").append(df.format(date)).append("',");
            else
                data.append("'',");
            tmp = df.format(date);
        }
        data.append(']');
        return data.toString();
    }

    @RequestMapping(value = "submit", method = RequestMethod.GET)
    public String getSubmitData(String stuNum) {
        List<IndexInfo> totalData = solutionMapper.getTotalData(stuNum);
        StringBuilder data = new StringBuilder("[");
        for (IndexInfo totalDatum : totalData) {
            data.append(totalDatum.getC()).append(",");
        }
        data.append("]");
        return data.toString();
    }

    @RequestMapping(value = "accept", method = RequestMethod.GET)
    public String getAcceptData(String stuNum){
        List<IndexInfo> totalData = solutionMapper.getTotalData(stuNum);
        List<IndexInfo> acceptData = solutionMapper.getAcceptData(stuNum);
        Map<String,String> totalmap = new HashMap<>();
        Map<String,String> acmap = new HashMap<>();
        for (IndexInfo totalDatum : totalData) {
            totalmap.put(totalDatum.getMd(),totalDatum.getC());
        }
        for (IndexInfo acceptDatum : acceptData) {
            acmap.put(acceptDatum.getMd(), acceptDatum.getC());
        }
        StringBuilder data = new StringBuilder("[");
        for (IndexInfo totalDatum : totalData) {
            if(acmap.get(totalDatum.getMd()) == null)
                data.append("0,");
            else
                data.append(acmap.get(totalDatum.getMd())).append(",");
        }
        data.append("]");
        return data.toString();
    }

    @RequestMapping(value = "allInfo", method = RequestMethod.GET)
    public String getPersonAllInfo(String stuNum){
        return getLabels(stuNum) + "|" + getSubmitData(stuNum) + "|" + getAcceptData(stuNum);
    }

    @RequestMapping(value = "piedata", method = RequestMethod.GET)
    public String getPieData(String stuNum){
        List<PersonInfoPie> list = new LinkedList<>();
        List<Integer> integers = solutionMapper.getPieData(stuNum);
        for(int i = 0 ; i < integers.size() ; i++){
            PersonInfoPie personInfoPie = new PersonInfoPie();
            personInfoPie.setValue(integers.get(i));
            personInfoPie.setColor(Constants.PIECOLORS[i]);
            personInfoPie.setHighlight(Constants.PIECOLORS[i]);
            personInfoPie.setLabel(Constants.PIELABELS[i]);
            list.add(personInfoPie);
        }
        String s = null;
        try {
            s = MapperUtils.obj2json(list);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return s;
    }
}
