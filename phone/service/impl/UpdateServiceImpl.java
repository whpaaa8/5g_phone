package com.phone.service.impl;

import com.csvreader.CsvReader;
import com.phone.pojo.Analysis;
import com.phone.pojo.Comment;
import com.phone.pojo.Phone;
import com.phone.service.AnalysisService;
import com.phone.service.CommentService;
import com.phone.service.PhoneService;
import com.phone.service.UpdateService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

@Service
public class UpdateServiceImpl implements UpdateService {
    @Autowired
    private PhoneService phoneService;
    @Autowired
    private CommentService commentService;
    @Autowired
    private AnalysisService analysisService;

    String path = "classpath:static/data/";

    @Override
    public int Update() throws IOException {
        // 第一参数：读取文件的路径 第二个参数：分隔符（不懂仔细查看引用百度百科的那段话） 第三个参数：字符集
        String InfoPath = ResourceUtils.getFile("classpath:static/data/"+"phone/info/Analyze_phones.csv").getAbsolutePath();
        CsvReader csvReader = new CsvReader(InfoPath, ',', Charset.forName("UTF-8"));
        csvReader.readHeaders();
        HashMap<String,String> map = new HashMap<>();
        while (csvReader.readRecord()) {
            String gid = csvReader.get("id");
            String type = csvReader.get("type");
//            String content = csvReader.get("评论内容");
            map.put(gid,type);
        }

        InfoPath = ResourceUtils.getFile(path+"phone/info/phones_info.csv").getAbsolutePath();
        csvReader = new CsvReader(InfoPath, ',', Charset.forName("UTF-8"));

        int count = phoneService.getCount();
        // 如果你的文件没有表头，这行不用执行
        // 这行不要是为了从表头的下一行读，也就是过滤表头
        csvReader.readHeaders();
        while (csvReader.readRecord())
        {
            count--;
            if (count == 0) break;
        }
        // 读取每行的内容
        int num = 0;
        while (csvReader.readRecord()) {
            num++;
            String brand = csvReader.get("品牌");
            String id = csvReader.get("id");
            String desc = csvReader.get("手机名称");
            String img = csvReader.get("图片");
            String link = csvReader.get("链接");
            //判断手机是否已经存在
            Boolean p = phoneService.isExist(id);
            if (p) continue;
            if (map.get(id).equals("BAN")) continue;
            //该手机不存在则更新
            Phone phone = new Phone(id,desc,link,img,brand);
            //存手机信息
            phoneService.save(phone);
            //存评论信息
            List<Comment> comments = getComments(id);
            commentService.batchSave(comments);
            //存分析信息
            analysisService.save(getAnalysis(id));
//            System.out.println(phone.toString());
        }
        return num;
    }

    @Override
    public Boolean UpdateById(String id) throws IOException {
        Boolean p = phoneService.isExist(id);
        System.out.println("Phone_id:"+id);

        //存手机信息
//        phoneService.save(phone);
        //存评论信息
        List<Comment> comments = getComments(id);
//        for (Comment c:comments)
//        {
//            System.out.println(c.toString());
//        }
        commentService.batchSave(comments);
        //存分析信息
//        System.out.println(getAnalysis(id).toString());
        analysisService.save(getAnalysis(id));
        return true;
    }

    public List<Comment> getComments(String id) throws IOException {
        String name = String.format("%s.csv",id);
        String InfoPath = ResourceUtils.getFile(path+"phone/comment/sel/"+name).getAbsolutePath();
        CsvReader csvReader = new CsvReader(InfoPath, ',', Charset.forName("UTF-8"));
        // 如果你的文件没有表头，这行不用执行
        // 这行不要是为了从表头的下一行读，也就是过滤表头
        csvReader.readHeaders();
        int idx = 1;
        List<Comment> comments = new ArrayList<>();
        // 读取每行的内容
        while (csvReader.readRecord()) {

            String username = csvReader.get("用户名");
            String type = csvReader.get("评论类型");
            String content = csvReader.get("评论内容");
            Comment comment = new Comment(id,Integer.toString(idx),type,content,username);
            idx++;
            comments.add(comment);
//            System.out.println(comment.toString());
        }
        return comments;
    }

    public Analysis getAnalysis(String id)
    {
        String pos_lda = String.format("phone/visualization/pos_lda_visualization_%s.html",id);
        String neg_lda = String.format("phone/visualization/neg_lda_visualization_%s.html",id);
        String pos_topic = String.format("phone/analysis/topic/pos_topics_%s.csv",id);
        String neg_topic = String.format("phone/analysis/topic/neg_topics_%s.csv",id);
        try {
            pos_topic = getTopic(pos_topic);
            neg_topic = getTopic(neg_topic);
        } catch (IOException e) {
            pos_topic = "NOT FUND!";
            neg_topic = "NOT FUND!";
        }
        String pos_wordcloud = String.format("phone/wordcloud/pos_%s.jpg",id);
        String neg_wordcloud= String.format("phone/wordcloud/neg_%s.jpg",id);
        return new Analysis(id,pos_wordcloud,neg_wordcloud,pos_lda,neg_lda,pos_topic,neg_topic);
    }

    public String getTopic(String p) throws IOException {
        String InfoPath = ResourceUtils.getFile(path+p).getAbsolutePath();
        CsvReader csvReader = new CsvReader(InfoPath, ',', Charset.forName("UTF-8"));
        csvReader.readHeaders();
        StringBuilder topic = new StringBuilder();
        int index = 1;
        while (csvReader.readRecord())
        {
            int len = csvReader.getColumnCount();
            StringBuilder s = new StringBuilder();
            s.append(index);
            s.append(": ");
            for (int i = 1 ; i < len;i++)
            {
                s.append(csvReader.get(i));
                s.append(",");
            }
            s.deleteCharAt(s.length()-1);
            s.append("\n");
            topic.append(s);
            index++;
        }

        return topic.toString();
    }

}
