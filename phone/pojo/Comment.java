package com.phone.pojo;

public class Comment {
    private String goods_id;
    private String comment_id;
    private String type;
    private String content;

    public Comment(String goods_id, String comment_id, String type, String content, String username) {
        this.goods_id = goods_id;
        this.comment_id = comment_id;
        this.type = type;
        this.content = content;
        this.username = username;
    }

    public String getGoods_id() {
        return goods_id;
    }

    public void setGoods_id(String goods_id) {
        this.goods_id = goods_id;
    }

    public String getComment_id() {
        return comment_id;
    }

    public void setComment_id(String comment_id) {
        this.comment_id = comment_id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    private String username;

    @Override
    public String toString() {
        return "Comment{" +
                "goods_id='" + goods_id + '\'' +
                ", comment_id='" + comment_id + '\'' +
                ", type='" + type + '\'' +
                ", content='" + content + '\'' +
                ", username='" + username + '\'' +
                '}';
    }
}
