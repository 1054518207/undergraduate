package edu.ytu.chen.pro.service.impl;

import edu.ytu.chen.pro.DAO.SolutionMapper;
import edu.ytu.chen.pro.entity.IndexInfo;
import edu.ytu.chen.pro.service.PersonInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestMapping;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

@Service
public class PersonInfoServiceImpl implements PersonInfoService {

    @Autowired
    private SolutionMapper solutionMapper;

    @Override
    public String getLabels(String stuNum){
        return null;
    }

    @Override
    public String getSubmitData(String stuNum) {
        List<IndexInfo> totalData = solutionMapper.getTotalData(stuNum);
        SimpleDateFormat df = new SimpleDateFormat("MMM", Locale.ENGLISH);
        String data = "[";
        String tmp = "";
        for (IndexInfo totalDatum : totalData) {
            Date date = new Date(new Long(totalDatum.getMd()));
            if (!tmp.equals(df.format(date)))
                System.out.print("'" + df.format(date) + "',");
            else
                System.out.print("'',");
            tmp = df.format(date);
        }
        System.out.println("]");
        System.out.print("[");
        for (IndexInfo totalDatum : totalData) {
            System.out.print(totalDatum.getC() + ",");
        }
        System.out.println("]");
        System.out.print("[");
        List<IndexInfo> acceptData = solutionMapper.getAcceptData("201758501101");
        for (IndexInfo acceptDatum : acceptData) {
            System.out.print(acceptDatum.getC()+",");
        }
        System.out.println("]");
        return null;
    }

    @Override
    public String getAcceptData(String stuNum) {
        return null;
    }
}
