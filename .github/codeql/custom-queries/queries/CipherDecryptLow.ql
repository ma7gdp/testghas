/**
 * @name Lower severity for cipher.decrypt
 * @description Treat uses of `cipher.decrypt(...)` as low severity findings.
 * @kind problem
 * @severity low
 * @id python/custom/cipher-decrypt-low
 */

import python

from CallExpr call, Attribute attribute
where
  call.getCallee() = attribute and
  attribute.getAttributeName() = "decrypt"

select call, "Call to decrypt() on an object (treated as low severity)."
