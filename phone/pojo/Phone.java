package com.phone.pojo;

public class Phone {
    private String goods_id;
    private String desc;
    private String link;
    private String img;
    private String brand;

    @Override
    public String toString() {
        return "Phone{" +
                "goods_id='" + goods_id + '\'' +
                ", desc='" + desc + '\'' +
                ", link='" + link + '\'' +
                ", img='" + img + '\'' +
                ", brand='" + brand + '\'' +
                '}';
    }

    public Phone(String goods_id, String desc, String link, String img, String brand) {
        this.goods_id = goods_id;
        this.desc = desc;
        this.link = link;
        this.img = img;
        this.brand = brand;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }


    public String getGoods_id() {
        return goods_id;
    }

    public void setGoods_id(String goods_id) {
        this.goods_id = goods_id;
    }

    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    public String getLink() {
        return link;
    }

    public void setLink(String link) {
        this.link = link;
    }

    public String getImg() {
        return img;
    }

    public void setImg(String img) {
        this.img = img;
    }



}
