package edu.ytu.chen.pro.controller;

import edu.ytu.chen.pro.DAO.SolutionMapper;
import edu.ytu.chen.pro.commons.MapperUtils;
import edu.ytu.chen.pro.entity.IndexInfo;
import edu.ytu.chen.pro.entity.IndexJsonInfo;
import edu.ytu.chen.pro.service.PythonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import tk.mybatis.mapper.common.Mapper;

import javax.servlet.http.HttpServletRequest;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Controller
public class IndexController {

    @Autowired
    private PythonService pythonService;

    @Autowired
    private SolutionMapper solutionMapper;

    @RequestMapping(value = {"", "index"}, method = RequestMethod.GET)
    public String getIndex(@RequestParam(required = false) HttpServletRequest httpServletRequest, Model model){
        String json = getDisplayInfo();
        if(json != null){
            model.addAttribute("data",json);
        }else{
            String s = "[{\"md\":\"2019-04-07\",\"c1\":\"891\",\"c2\":\"168\"},{\"md\":\"2019-04-06\",\"c1\":\"1424\",\"c2\":\"405\"},{\"md\":\"2019-04-05\",\"c1\":\"1527\",\"c2\":\"463\"},{\"md\":\"2019-04-04\",\"c1\":\"1194\",\"c2\":\"436\"}]";
            model.addAttribute("data",s);
        }
        return "index";
    }

    /**
     * 获取主页展示信息
     * @return 主页展示所需JSON数据
     */
    private String getDisplayInfo(){
        List<IndexInfo> total = null;
        try{
            total = solutionMapper.getTotalIndexInfo();
        }catch (Exception e) {
            return null;
        }
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
        String text = null;
        try {
            text = MapperUtils.obj2json(infos);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return text;
    }
}
