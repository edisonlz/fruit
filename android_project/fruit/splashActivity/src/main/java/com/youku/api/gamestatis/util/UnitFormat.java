package com.youku.api.gamestatis.util;

public class UnitFormat {

	public static String toTenThousand(double data){
		return String.format("%.1f万", data/10000);
	}
	
	public static String toTenThousand(int data){
		return String.format("%.1f万", data/10000.0);
	}
}
