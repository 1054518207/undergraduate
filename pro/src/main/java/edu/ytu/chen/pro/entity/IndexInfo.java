package edu.ytu.chen.pro.entity;

import lombok.Data;

import java.io.Serializable;

/**
 * 所有时间戳SQL语句使用
 */

@Data
public class IndexInfo implements Serializable {

    /**
     * 主页信息，用于展示主页面
     * sql：SELECT UNIX_TIMESTAMP(date(in_date))*1000 md,count(1) c FROM (select * from solution order by solution_id desc limit 8000) solution  where result<13 group by md order by md desc limit 200
     */
    String md;

    String c;
}
