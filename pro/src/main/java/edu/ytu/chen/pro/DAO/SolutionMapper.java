package edu.ytu.chen.pro.DAO;

import edu.ytu.chen.pro.entity.IndexInfo;
import edu.ytu.chen.pro.entity.Solution;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import tk.mybatis.MyMapper;

import java.util.List;

public interface SolutionMapper extends MyMapper<Solution> {

    /**
     * 返回总共提交数
     * @return
     */
    @Select("SELECT UNIX_TIMESTAMP(date(in_date))*1000 md,count(1) c FROM (select * from solution order by solution_id desc limit 8000) solution  where result<13 group by md order by md desc limit 200")
    List<IndexInfo> getTotalIndexInfo();

    @Select("SELECT UNIX_TIMESTAMP(date(in_date))*1000 md,count(1) c FROM  (select * from solution order by solution_id desc limit 8000) solution where result=4 group by md order by md desc limit 200")
    List<IndexInfo> getCorrectIndexInfo();

    /**
     * 获取时间戳所有的提交总量
     * @return Indexinfo列表，md表示时间戳，c表示统计量
     */
    @Select("SELECT UNIX_TIMESTAMP(date(in_date))*1000 md,count(1) c FROM `solution` where  `user_id`=#{stuNum}  group by md order by md desc")
    List<IndexInfo> getTotalData(@Param("stuNum") String stuNum);

    /**
     * 获取时间戳所有的AC总量
     * @return Indexinfo列表，md表示时间戳，c表示统计量
     */
    @Select("SELECT UNIX_TIMESTAMP(date(in_date))*1000 md,count(1) c FROM `solution` where  `user_id`=#{stuNum} and result=4 group by md order by md desc")
    List<IndexInfo> getAcceptData(@Param("stuNum") String stuNum);

    /**
     * 获取个人整个提交信息
     * @param stuNum 学号
     * @return 整形信息列表
     */
    @Select("SELECT count(1) as info FROM solution WHERE `user_id`=#{stuNum} AND result>=4 group by result order by result")
    List<Integer> getPieData(@Param("stuNum") String stuNum);
}