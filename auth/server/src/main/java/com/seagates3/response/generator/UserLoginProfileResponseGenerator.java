/*
 * COPYRIGHT 2019 SEAGATE LLC
 *
 * THIS DRAWING/DOCUMENT, ITS SPECIFICATIONS, AND THE DATA CONTAINED
 * HEREIN, ARE THE EXCLUSIVE PROPERTY OF SEAGATE TECHNOLOGY
 * LIMITED, ISSUED IN STRICT CONFIDENCE AND SHALL NOT, WITHOUT
 * THE PRIOR WRITTEN PERMISSION OF SEAGATE TECHNOLOGY LIMITED,
 * BE REPRODUCED, COPIED, OR DISCLOSED TO A THIRD PARTY, OR
 * USED FOR ANY PURPOSE WHATSOEVER, OR STORED IN A RETRIEVAL SYSTEM
 * EXCEPT AS ALLOWED BY THE TERMS OF SEAGATE LICENSES AND AGREEMENTS.
 *
 * YOU SHOULD HAVE RECEIVED A COPY OF SEAGATE'S LICENSE ALONG WITH
 * THIS RELEASE. IF NOT PLEASE CONTACT A SEAGATE REPRESENTATIVE
 * http://www.seagate.com/contact
 *
 * Original author: Abhilekh Mustapure <abhilekh.mustapure@seagate.com>
 * Original creation date: 22-May-2019
 */
package com.seagates3.response.generator;

import java.util.ArrayList;
import java.util.LinkedHashMap;

import com.seagates3.model.User;
import com.seagates3.response.ServerResponse;
import com.seagates3.response.formatter.xml.XMLResponseFormatter;

public
class UserLoginProfileResponseGenerator extends AbstractResponseGenerator {

 public
  ServerResponse generateCreateResponse(User user) {
    LinkedHashMap responseElements = new LinkedHashMap();
    responseElements.put("UserName", user.getName());
    responseElements.put("UserId", user.getId());
    return new XMLResponseFormatter().formatCreateResponse(
        "CreateLoginProfile", "LoginProfile", responseElements, "0000");
  }

  /**
   * Below method will generate 'GetLoginProfile' response
   *
   * @param user
   * @return LoginProfile (username and password) of the requested user
   */
 public
  ServerResponse generateGetResponse(User user) {
    LinkedHashMap<String, String> responseElements = new LinkedHashMap<>();
    ArrayList<LinkedHashMap<String, String>> userMembers = new ArrayList<>();
    // TODO:Password creation Date not yet set in USER pojo
    responseElements.put("UserName", user.getName());
    // responseElements.put("CreateDate", "2019-06-10T07:38:07Z");
    userMembers.add(responseElements);
    return new XMLResponseFormatter().formatGetResponse(
        "GetLoginProfile", "LoginProfile", userMembers, "0000");
  }
}
